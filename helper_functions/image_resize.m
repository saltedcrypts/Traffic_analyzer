loc_path='~/Traffic_analyzer/images'
listing=dir('~/Traffic_analyzer/images')
for i=3:size(listing)
    listing(i).name
    read_img=imread(strcat(loc_path,'/',listing(i).name))
    read_img=imresize(read_img,[20,20]);
    imwrite(read_img,strcat(loc_path,'/',listing(i).name))
    %size(read_img(:))
    %imshow(read_img)
end
        