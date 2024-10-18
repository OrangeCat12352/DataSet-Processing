# --------------------------------------------------------#
#   该文件用于对原始遥感图像训练数据进行裁切，生成固定大小的patches,适用于HBB(Horizontal Bounding Box)
# --------------------------------------------------------#
import cv2
import os
import numpy as np
import glob


def split(imgname, dirsrc, dirdst, subsize=800, gap=200, ext='.png'):
    """
    imgname:   待裁切图像名（带扩展名）
    dirsrc:    待裁切的图像保存目录的上一个目录，默认图像与标注文件在一个文件夹下，图像在images下，标注在labelTxt下，标注文件格式为每行一个gt,
               格式为xmin,ymin,xmax,ymax,class,想读其他格式自己动手改
    dirdst:    裁切的图像保存目录的上一个目录，目录下有images,labelTxt两个目录分别保存裁切好的图像或者txt文件，
               保存的图像和txt文件名格式为 oriname_min_ymin.png(.txt),(xmin,ymin)为裁切图像在原图上的左上点坐标,txt格式和原文件格式相同
    subsize:   裁切图像的尺寸，默认为正方形，想裁切矩形自己动手改
    gap:       相邻行或列的图像重叠的宽度
    iou_thresh:小于该阈值的BBGT不会保存在对应图像的txt中（在图像过于边缘或与图像无交集）
    ext:       保存图像的格式
    """
    img = cv2.imread(os.path.join(os.path.join(dirsrc,'1'), imgname), -1)  # 读取图片信息

    img_h,img_w = img.shape[:2]  # 得到空间宽高
    top = 0  # 图片上方标量
    reachbottom = False  # 到达底部标记
    while not reachbottom:  # 若没到达底部
        reachright = False  # 到达最右标记
        left = 0  # 图片左边标量
        if top + subsize >= img_h:  # 若下方超界，则从下往上裁剪
            reachbottom = True
            top = max(img_h-subsize,0)
        while not reachright:  # 若没到达右边
            if left + subsize >= img_w:  # 若右方超界，则从右往左裁剪
                reachright = True
                left = max(img_w-subsize,0)
            imgsplit = img[top:min(top+subsize,img_h),left:min(left+subsize,img_w)]  # 裁剪图片
            if imgsplit.shape[:2] != (subsize,subsize):  # 若长度跟预设不等， 补充黑框
                try:  # 若为多通道
                    template = np.zeros((subsize, subsize, imgsplit.shape[2]), dtype=np.uint8)
                    template[0:imgsplit.shape[0], 0:imgsplit.shape[1]] = imgsplit
                    imgsplit = template
                except:  # 若为单通道
                    template = np.zeros((subsize,subsize),dtype=np.uint8)
                    template[0:imgsplit.shape[0],0:imgsplit.shape[1]] = imgsplit
                    imgsplit = template
            imgrect = np.array([left,top,min(left+subsize,img_w),min(top+subsize,img_h)]).astype('float32')  # 得到图片切割位置

            # print(len(BBpatch))
            cv2.imwrite(os.path.join(os.path.join(dirdst, '1'),
                                     imgname.split('.')[0] + '_' + str(left) + '_' + str(top) + ext), imgsplit)  # 保存图片

            left += subsize-gap  # 右滑
        top += subsize-gap  # 下滑


if __name__ == '__main__':
    import tqdm
    dirsrc= r'D:\Models\DataSet Processing'      # 待裁剪图像所在目录的上级目录，图像在images文件夹下，标注文件在labelTxt下
    dirdst= dirsrc + '//' + 'data_crop'   # 裁剪结果存放目录，格式和原图像目录一样
    if not os.path.exists(dirdst):  # 创建裁剪保存文件夹
        os.mkdir(dirdst)
    if not os.path.exists(os.path.join(dirdst, '1')):
        os.mkdir(os.path.join(dirdst, '1'))


    subsize = 256  # 裁剪后的图像大小
    gap = 0  # 允许重叠的大小
    ext = '.png'  # 保存图像尾缀

    imglist = glob.glob(f'{dirsrc}/1/*.png')  # 得到文件夹下所有图片的路径
    imgnameList = [os.path.split(imgpath)[-1] for imgpath in imglist]  # 得到所有图片的名称（含尾缀）
    for imgname in tqdm.tqdm(imgnameList):  # 迭代器输出进度，得到单个图像的名称（含尾缀）
        split(imgname, dirsrc, dirdst, subsize, gap, ext)
        #     图片名称  图片路径  保存路径  裁剪尺寸  重叠长度  iou阈值  保存尾缀

