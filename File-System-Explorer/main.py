import os 
from FAT32 import FAT32
if __name__ == "__main__":
    volumes = [chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")]
    print("Available:")
    for i in range(len(volumes)):
     print(f"{i + 1}/", volumes[i])
    try:
        choice = int(input("Volume: "))
    except Exception as e:
        print(f"[ERROR] {e}")
        exit()
    
    # Testing for FAT32
    volume_name = volumes[choice - 1]
    if FAT32.check_fat32(volume_name):
        vol = FAT32(volume_name)
        vol.show()
    else:
        print("Unsupported")
        exit()