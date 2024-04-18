from typing import List
import os
import cv2

class Utils():

    def getFilesFromDirectory(self, directoryPath: str) -> List[str]:
        file_names: List[str] = []
        for filename in os.listdir(directoryPath):
            if os.path.isfile(os.path.join(directoryPath, filename)):
                file_names.append(filename)

        return file_names

    
    def getBarcodeFromImage(self, image: str):
        img = cv2.imread(f'Input Files/{image}')
        bd = cv2.barcode.BarcodeDetector()

        retval, decoded_info, decoded_type = bd.detectAndDecode(img)

        return retval
    
    
    def putNameAndBarecodeIntoTxtFile(self, imageName: str, text_file_path: str, barcode):
        try:
            with open(text_file_path, 'a') as text_file:
                text_file.write(f"{imageName} -> {barcode}\n")
            
        except Exception as e:
            print("Error:", str(e))



    def delete_images(self, directory):
        # Get list of all files in the directory
        files = os.listdir(directory)
        
        # Iterate through each file
        for file in files:
            # Check if the file is an image file
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Construct the full path of the file
                file_path = os.path.join(directory, file)
                # Delete the image file
                os.remove(file_path)