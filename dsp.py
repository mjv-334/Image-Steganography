from PIL import Image 

#funtion for encoding data
def encode_lsb_image(scrt_path,cvr_path,size):
    rq_ht,rq_wd=256,256
    if len(size)>4:  #makes sure secret image adheres to size
       size=size.split('x'or 'X')
       rq_ht=size[1]
       rq_wd=size[0]

    #opnes secret image and cover image for pixel manipulations
    scrt_image = Image.open(scrt_path).convert("L")
    cvr_image = Image.open(cvr_path).convert("L")

    encoded_image = cvr_image.copy() #Creates new image to save the encoded image

    scrt_image=scrt_image.resize((rq_wd,rq_ht))
    
    #loading pixel map of both images
    base_pixels=cvr_image.load()
    encode_pixels=scrt_image.load()
    w_cvr, h_cvr = cvr_image.size

    #clearing Lsb of cover image and inserting Msb of secret image 
    for i in range(w_cvr):
      for j in range(h_cvr):
        base_px= base_pixels[i,j]
        encode_px=encode_pixels[i,j]
        new_pixel=(base_px& 0xFE )| (encode_px>>7)      
        encoded_image.putpixel((i, j), new_pixel)
        
    encoded_image.save("Encoded.png") #save encoded image
    encoded_image.show()   #opens encoded image for viewing
   
#funtion to decode data
def decode_lsb_image(encoded_image_path, output_path):
    # Open the encoded image
    encoded_image = Image.open(encoded_image_path).convert('RGB')

    # Create a new image to store the extracted secret
    decoded_image = Image.new("RGB", encoded_image.size)

    #loads pixel map for pixel manipulation
    encoded_pixel= encoded_image.load()
    decoded_pixel=decoded_image.load()

    #isolating Lsb of encoded image and extractiong data
    for x in range(encoded_image.width):
        for y in range(encoded_image.height):
            r, g, b = encoded_pixel[x, y]
            # Extract the LSB (least significant bit)
            r_secret = (r & 1) <<7
            g_secret = (g & 1) << 7
            b_secret = (b & 1) << 7
            decoded_pixel[x, y] = (r_secret, g_secret, b_secret)

    
    decoded_image.save(output_path) # Save the decoded image
    decoded_image.show()    #showing the decoded image

#Main program 
while True:
    Option=int(input("Choose Option: \n1.Encode an image.\n2.Decode an image.\n3.Exit\n"))
    if Option==1:
        scrt_path=str(input("Enter file name of picture to be encoded (eg:Image.png) : "))
        cvr_path=str(input("Enter file name of cover image (eg:cover.png) : "))
        size=(input("Input the required pixel size of image to be encoded(default size-256x256) : "))
        encode_lsb_image(scrt_path,cvr_path,size)
        print("Encoding complete")
    elif Option==2:
        print("File will be saved in parent folder by default")
        encoded_image_path=str(input("Input the name of file to be decoded(eg:Encoded.png): "))
        output_path=str(input("Input name for decoded file: "))
        decode_lsb_image(encoded_image_path, output_path)
    elif Option==3:
        exit()
    else:
        print("wrong option")