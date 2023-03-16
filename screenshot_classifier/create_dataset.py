import os
import shutil

def create_train_val_test(train_pct, val_pct, test_pct, train_dir, val_dir, test_dir):
    # Loop over the subdirectories ("good_images" and "bad_images")
    for subdir in os.listdir(src_dir):
        subdir_path = os.path.join(src_dir, subdir)
        if os.path.isdir(subdir_path):
            # Count the number of images in the current subdirectory
            num_images = len(os.listdir(subdir_path))
            
            # Calculate the number of images to use for each set
            num_train = int(num_images * train_pct)
            num_val = int(num_images * val_pct)
            
            # Create the destination directories for each set
            os.makedirs(os.path.join(train_dir, subdir), exist_ok=True)
            os.makedirs(os.path.join(val_dir, subdir), exist_ok=True)
            os.makedirs(os.path.join(test_dir, subdir), exist_ok=True)
            
            # Copy images into the training set
            for i in range(num_train):
                src_file = os.path.join(subdir_path, os.listdir(subdir_path)[i])
                dst_file = os.path.join(train_dir, subdir, os.listdir(subdir_path)[i])
                shutil.copy(src_file, dst_file)
                
            # Copy images into the validation set
            for i in range(num_train, num_train+num_val):
                src_file = os.path.join(subdir_path, os.listdir(subdir_path)[i])
                dst_file = os.path.join(val_dir, subdir, os.listdir(subdir_path)[i])
                shutil.copy(src_file, dst_file)
                
            # Copy images into the test set
            for i in range(num_train+num_val, num_images):
                src_file = os.path.join(subdir_path, os.listdir(subdir_path)[i])
                dst_file = os.path.join(test_dir, subdir, os.listdir(subdir_path)[i])
                shutil.copy(src_file, dst_file)


def create_train_test(train_pct, train_dir, test_dir):
    # Loop over the subdirectories ("good_images" and "bad_images")
    for subdir in os.listdir(src_dir):
        subdir_path = os.path.join(src_dir, subdir)
        if os.path.isdir(subdir_path):
            # Count the number of images in the current subdirectory
            num_images = len(os.listdir(subdir_path))
            
            # Calculate the number of images to use for each set
            num_train = int(num_images * train_pct)
            
            # Create the destination directories for each set
            os.makedirs(os.path.join(train_dir, subdir), exist_ok=True)
            os.makedirs(os.path.join(test_dir, subdir), exist_ok=True)
            
            # Copy images into the training set
            for i in range(num_train):
                src_file = os.path.join(subdir_path, os.listdir(subdir_path)[i])
                dst_file = os.path.join(train_dir, subdir, os.listdir(subdir_path)[i])
                shutil.copy(src_file, dst_file)
                
            # Copy images into the test set
            for i in range(num_train, num_images):
                src_file = os.path.join(subdir_path, os.listdir(subdir_path)[i])
                dst_file = os.path.join(test_dir, subdir, os.listdir(subdir_path)[i])
                shutil.copy(src_file, dst_file)



    
if __name__ == "__main__":
    # Set the source directory where your images are located
    src_dir = 'original_images/'
    
    # Set the destination directories for training, validation, and test sets
    train_dir = 'dataset/train/'
    #val_dir = 'dataset/val/'
    test_dir = 'dataset/test/'
    
    # Set the percentage of images to use for each set
    #train_pct = 0.7
    #val_pct = 0.15
    #test_pct = 0.15
    #create_train_val_test(train_pct, val_pct, test_pct, train_dir, val_dir, test_dir)

    train_pct = 0.75
    create_train_test(train_pct, train_dir, test_dir)
   