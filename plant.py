
import os
import argparse
from plantcv import plantcv as pcv


def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug",
                        help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.",
                        default=None)
    args = parser.parse_args()
    return args


def main():
    args = options()

    pcv.params.debug = args.debug  
    pcv.params.debug_outdir = args.outdir  

    img, path, filename = pcv.readimage(filename=args.image)

   
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')

    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

    b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')
    b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')

    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

    masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')

    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    ab_fill = pcv.fill(bin_img=ab, size=200)

    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')

    id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)

    roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=100, y=100, h=200, w=200)

    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')

    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)


    outfile = False
    if args.writeimg == True:
        outfile = os.path.join(args.outdir, filename)

    shape_imgs = pcv.analyze_object(img=img, obj=obj, mask=mask)

    boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, line_position=1680)

    color_histogram = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type='all')

    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=s, mask=mask, cmap='jet')

    pcv.print_results(filename=args.result)

if __name__ == '__main__':
    main()

