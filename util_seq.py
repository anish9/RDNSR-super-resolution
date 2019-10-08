class custom_datagen(tf.keras.utils.Sequence):
    def __init__(self,source_list,batch_size,replace_comp = (None,None), shuffle=True):
        self.source_list  =  source_list
        self.batch_size   =  batch_size
        self.shuffle      =  shuffle
        self.replace_comp =  replace_comp
        self.indexes      = np.arange(len(self.source_list))
        
        
    def __len__(self):
        return int(np.floor(len(self.source_list) / self.batch_size))
    
    def on_epoch_end(self):
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
    
    def __getitem__(self, index):
        xb = []
        yb = []
        inds = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        list_x = [self.source_list[k] for k in inds]
        passedx,passedy = self.Datagen(list_x)
        jbs = dict()
        for t,v in zip(passedx,passedy):
            img = cv2.imread(t,-1)
            img = self.image_resize(img,width=300)
            height_o_image,width_o_image = img.shape[0],img.shape[1]
            if height_o_image % 2 != 0:
                height_o_image = height_o_image-1
            if width_o_image % 2 != 0:
                width_o_image = width_o_image-1
            jbs["width"] = width_o_image*2
            jbs["height"] = height_o_image*2
            img = cv2.resize(img,(width_o_image,height_o_image))
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            masks = cv2.imread(v,-1)
            masks = cv2.resize(masks,(jbs["width"],jbs["height"]))
            masks = cv2.cvtColor(masks,cv2.COLOR_BGR2RGB)
            xb.append(img)
            yb.append(masks)
        
        xarr = np.array(xb)/127.5
        xarr = xarr-1
        yarr = np.array(yb)/127.5
        yarr = yarr-1
        return xarr,yarr
    
    def Datagen(self,complist):
        source_name,target_name = self.replace_comp
        x_list = complist
        y_list = [q.replace(source_name,target_name) for q in complist]
        return x_list,y_list
    
    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        resized = cv2.resize(image, dim, interpolation = inter)
        return resized
