################################################################################################
#                                                                                              #
# code adapted from https://github.com/kittles/cartogrampy/blob/master/cartogrampy/generate.py #
#                                                                                              #
################################################################################################

import itertools as itr
import numpy as np
import subprocess as sp
from PIL import Image, ImageDraw
import time
import os


this_dir = os.path.abspath(os.path.dirname(__file__))
tmp_dir = os.path.join(this_dir, "tmp")


def prod(xs, ys, margin=0):
    return itr.product(range(xs - margin), range(ys - margin))


def generate_control_points(w, h, w_cnt, h_cnt):
    # generates a grid of control points
    # these are points of the form (x, y), and the x and y
    # initially correspond to the x and y indicies for the point.
    # the idea is that the point's indicies encode its "initial position"
    # and the point itself encodes its resulting position after displacement.
    # this seems a little crappy, maybe there is a more canonical way
    # of doing this.
    cps = np.zeros((h_cnt, w_cnt, 2))
    xs = np.linspace(0, w, w_cnt)
    ys = np.linspace(0, h, h_cnt)
    for x, y in prod(w_cnt, h_cnt):
        cps[y, x] = np.array([xs[x], ys[y]])
    return cps


def cp_rect(x, y, cps):
    # get a rect from a specific control point
    # uses the control point down and to the right of it
    # PIL uses this form of rectangle for the initial sections when
    # doing mesh transforms
    top_left = cps[y, x]
    bottom_right = cps[y + 1, x + 1]
    return (
        int(top_left[0]),
        int(top_left[1]),
        int(bottom_right[0]),
        int(bottom_right[1]),
    )


def cp_quad(x, y, cps):
    # a quadrilateral built from the south, south east, and east neighbors
    # this is the format PIL expects for the target quads that initial rects
    # get mapped to.
    points = (
        cps[y, x],
        cps[y + 1, x],
        cps[y + 1, x + 1],
        cps[y, x + 1],
    )
    return tuple([int(i) for point in points for i in point])


def displace_point(x, y, vec, mesh):
    # this is useful for showing how a point has shifted
    mesh[y, x] += vec
    return mesh[y, x]

def cartogram(img, z, clean=True):
    #check if machine is windows, if not, switch to wsl
    c_start = time.perf_counter()
    w, h = img.width, img.height
    print("\n==== Generating a new cartogram with shape w: {} h: {} ====".format(w, h))

    # write z to file
    print("\npreparing z data")
    ts = time.perf_counter()
    z_fp = os.path.join(tmp_dir, "z.dat")
    with open(z_fp, "w") as fh:
        for row in z:
            fh.write(" ".join([str(i) for i in row]) + "\n")
    print("...took {:.2f} seconds".format(time.perf_counter() - ts))

    # generate displacement data
    print("\ngenerating preliminary transforms from z data")
    ts = time.perf_counter()
    disp_fp = os.path.join(tmp_dir, "disp.dat")
    cmd = "cart {} {} {} {}".format(w, h, z_fp, disp_fp)
    sp.run(cmd, shell=True)
    print("...took {:.2f} seconds".format(time.perf_counter() - ts))

    print("\npreparing input points")
    ts = time.perf_counter()
    points_fp = os.path.join(tmp_dir, "points.txt")
    with open(points_fp, "w") as fh:
        for x, y in itr.product(np.linspace(0, w - 1, w), np.linspace(0, h - 1, h)):
            fh.write("{} {}\n".format(x, y))
    print("...took {:.2f} seconds".format(time.perf_counter() - ts))

    print("\ngenerating transformed points from input points")
    ts = time.perf_counter()
    points_disp_fp = os.path.join(tmp_dir, "points_disp.txt")
    cmd = "cat {} | interp {} {} {} > {}".format(
        points_fp, w, h, disp_fp, points_disp_fp
    )
    sp.run(cmd, shell=True)
    print("...took {:.2f} seconds".format(time.perf_counter() - ts))

    # use data to displace
    print("\ngenerating image transform mesh")
    ts = time.perf_counter()
    w_cnt, h_cnt = w, h
    control_points = generate_control_points(w, h, w_cnt, h_cnt)
    deformed_points = control_points.copy()

    pts = open(points_fp, "r")
    pts_dsp = open(points_disp_fp, "r")

    for pt, pt_dsp in zip(pts, pts_dsp):
        x, y = [float(i) for i in pt.split(" ")]
        xd, yd = [float(i) for i in pt_dsp.split(" ")]
        dsp_vec = np.array([x - xd, y - yd])
        displace_point(int(x), int(y), dsp_vec, deformed_points)

    transforms = []
    for x, y in prod(w_cnt, h_cnt, 1):
        transforms.append(
            (cp_rect(x, y, control_points), cp_quad(x, y, deformed_points))
        )
    print("...took {:.2f} seconds".format(time.perf_counter() - ts))

    # apply transforms
    print("\ntransforming image")
    ts = time.perf_counter()
    img = img.transform(img.size, Image.MESH, transforms, Image.BILINEAR)
    print("...took {:.2f} seconds".format(time.perf_counter() - ts))

    if clean:
        print("\ncleaning up temporary files")
        os.remove(z_fp)
        os.remove(disp_fp)
        os.remove(points_fp)
        os.remove(points_disp_fp)

    print("\nDONE ...{:.2f} seconds total".format(time.perf_counter() - c_start))
    img.save(os.path.join("project_images", "cartogram_tmp.png"), quality=85)
    return img
