# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:11:59 2021

@author: bcyat
"""
import numpy as np
import collections

path = 'code/Big_dataset/images_test.txt'

def im_txt_parse(path): 
    BaseImage = collections.namedtuple(
        "Image", ["id", "qvec", "tvec", "camera_id", "name", "xys", "point3D_ids"])
    
    def qvec2rotmat(qvec):
        return np.array([
            [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
              2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
              2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
            [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
              1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
              2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
            [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
              2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
              1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])
    
    class Image(BaseImage):
        def qvec2rotmat(self):
            return qvec2rotmat(self.qvec)
    
    def read_images_text(path):
        """
        see: src/base/reconstruction.cc
            void Reconstruction::ReadImagesText(const std::string& path)
            void Reconstruction::WriteImagesText(const std::string& path)
        """
        images = {}
        with open(path, "r") as fid:
            while True:
                line = fid.readline()
                if not line:
                    break
                line = line.strip()
                if len(line) > 0 and line[0] != "#":
                    elems = line.split()
                    image_id = int(elems[0])
                    qvec = np.array(tuple(map(float, elems[1:5])))
                    tvec = np.array(tuple(map(float, elems[5:8])))
                    camera_id = int(elems[8])
                    image_name = elems[9]
                    elems = fid.readline().split()
                    xys = np.column_stack([tuple(map(float, elems[0::3])),
                                           tuple(map(float, elems[1::3]))])
                    point3D_ids = np.array(tuple(map(int, elems[2::3])))
                    images[image_id] = Image(
                        id=image_id, qvec=qvec, tvec=tvec,
                        camera_id=camera_id, name=image_name,
                        xys=xys, point3D_ids=point3D_ids)
        return images
    
    imagestxt1 = read_images_text(path)
    
    posestxt = np.zeros(shape = (1800,7))
    count = 0
    
    for i in range(1800):
        try:
            posestxt[i,0:3] = imagestxt1[i+1][2]
            posestxt[i,3:8] = imagestxt1[i+1][1]
        except:
            count += 1
            print('no pose for Image ' + str(i))
    
    imagestxt = posestxt[~np.all(posestxt == 0, axis=1)]
    return imagestxt

dir_parse = im_txt_parse(path)

def qvec2rotmat(qvec):
        return np.array([
            [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
              2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
              2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
            [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
              1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
              2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
            [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
              2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
              1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])


rotdict = {}
cartarr = np.zeros(shape = (1751,3))

for i in range(len(dir_parse)):
    qvec = dir_parse[i][3:]
    rot = qvec2rotmat(qvec)
    rotdict[i] = rot
    cart = np.matmul(rot,dir_parse[i,0:3])
    cartarr[i] = cart

path = 'code/Big_dataset/poses.txt'
text_file = open(path, "r")
lines = text_file.read().splitlines()
#lines = np.array(lines,ndmin=2).transpose()
poses = np.empty(shape=(len(lines),8),dtype='float') 

for i in range(len(lines)): 
    poses[i,:] = lines[i].split(' ')

#poses = int(poses)


untrans = poses
poses[:,1:4] = cartarr[:,:]

untrans[:,1:4] = dir_parse[:,0:3]
poses[:,1:4] = cartarr[:,:]
np.savetxt('code/Big_dataset/cart.txt',poses,fmt='%f')
#np.savetxt('code/Big_dataset/untrans.txt',untrans,fmt='%f')
    