import cv2
import os

def register_face():
    # Rasmlar saqlanadigan papka
    data_path = "data/faces"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Terminaldan ID ni so'rash
    user_id = input("O'quvchi terminal_id raqamini kiriting (masalan: 100): ")
    
    cap = cv2.VideoCapture(0)
    print("Kameraga qarang. Rasmga olish uchun 's' ni, chiqish uchun 'q' ni bosing.")

    while True:
        ret, frame = cap.read()
        cv2.imshow('Yuzni ro\'yxatga olish', frame)

        key = cv2.waitKey(1)
        if key == ord('s'): # 's' bosilsa rasmga oladi
            img_name = f"{data_path}/user_{user_id}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"✅ Rasm saqlandi: {img_name}")
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_face()
