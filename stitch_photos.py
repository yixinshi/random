#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import os
import fnmatch
import argparse

from PIL import Image

def merge_images(filename, w, h, W, H):
    image = Image.open(filename)
    (width1, height1) = image.size

    print("width: %d, height: %d" % (width1, height1))
    num_w = int(W / w)
    num_h = int(H / h)
    print("num_w %d, num_h %d" % (num_w, num_h))
    canvas_width = int(width1 * W / w)
    canvas_height = int(height1 * H / h)
    print("width: %d, height: %d" % (canvas_width, canvas_height))

    result = Image.new('RGB', (canvas_width, canvas_height), color=(255,255,255,0))
    for w in range(0, num_w):
        for h in range(0, num_h):
            result.paste(im=image, box=(w * width1, h * height1))
    return result

def resize2size(filename, min_pixel):
    image = Image.open(filename)
    w, h = image.size
    min_side = min(w, h)
    if min_side < min_pixel: return image
    r = float(min_side / min_pixel)
    print("ratio: %f" % r)
    new_w, new_h = int(w / r), int(h / r)
    print("new w: %d, new h %d" %(new_w, new_h))
    return image.resize((new_w, new_h))


def main():
  for root, dir, files in os.walk(FLAGS.source_dir):
    for items in fnmatch.filter(files, "*.JPG"):
      new_pic_name = os.path.join(FLAGS.output_dir, FLAGS.prefix + items)
      print("converting %s ..." % items)
      new_pic = resize2size(items, FLAGS.min_pixel)
      new_pic.save(new_pic_name)
      print("saving to %s ...done" % new_pic_name)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")

  parser.add_argument(
      "--prefix",
      type=str,
      default="anon_",
      help="Preprocssing scheme: 1d for strokes and 2d for images.")

  parser.add_argument(
      "--source_dir",
      type=str,
      default=".",
      help="Directory where the ndjson files are stored.")

  parser.add_argument(
      "--output_dir",
      type=str,
      default=".",
      help="Directory where to store the output TFRecord files.")

  parser.add_argument(
      "--min_pixel",
      type=int,
      default=2240,
      help="How many items per class to load for training.")

  parser.add_argument(
      "--output_shards",
      type=int,
      default=10,
      help="Number of shards for the output.")

  parser.add_argument(
      "--num_classes",
      type=int,
      default=0,
      help="Number of classes for the training. 0 means all")

  parser.add_argument(
      "--stat_only",
      type="bool",
      default="False",
      help="Whether to do stat analysis of the input data only")

  FLAGS, unparsed = parser.parse_known_args()
  main()
