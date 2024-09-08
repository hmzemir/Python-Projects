import cv2
import pytesseract
import sqlite3

# Tesseract yolu (sisteminizdeki yola göre ayarlayın)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_plate_number(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Plaka tespiti için gereken ön işleme (örneğin, gürültü azaltma)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, config='--psm 8')
    return text.strip()

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        plate_number = extract_plate_number(frame)
        # Veritabanına kaydetme
        conn = sqlite3.connect('vehicle_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicles (plate, type) VALUES (?, ?)", (plate_number, 'Unknown'))
        conn.commit()
        conn.close()
        
        # Görüntü ve plaka numarası ekrana yazdırma
        cv2.imshow('Vehicle Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'videos/cars.mp4'
    process_video(video_path)
