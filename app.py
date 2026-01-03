import cv2
import numpy as np
import time
import winsound
import os

# Alarm file
ALARM_FILE = os.path.join("assets", "alarm.wav")

def beep_alert():
    """Plays the alarm sound asynchronously."""
    try:
        winsound.PlaySound(ALARM_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception as e:
        print("Error playing alarm:", e)

def draw_rounded_rectangle(img, pt1, pt2, color, thickness, radius=20):
    """Draw a rounded rectangle"""
    x1, y1 = pt1
    x2, y2 = pt2
    
    # Draw rectangles
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
    
    # Draw circles for corners
    cv2.circle(img, (x1 + radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y1 + radius), radius, color, thickness)
    cv2.circle(img, (x1 + radius, y2 - radius), radius, color, thickness)
    cv2.circle(img, (x2 - radius, y2 - radius), radius, color, thickness)

def draw_modern_ui(img, eye_state, eye_ratio, eye_closed_time, faces):
    """Draw modern, professional UI overlay"""
    h, w = img.shape[:2]
    
    # Create semi-transparent overlay for header
    overlay = img.copy()
    
    # Modern gradient-like header (darker at top)
    for i in range(100):
        alpha = 0.7 - (i * 0.005)
        cv2.rectangle(overlay, (0, i), (w, i+1), (20, 20, 20), -1)
    
    cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)
    
    # Top header bar with accent line
    cv2.rectangle(img, (0, 0), (w, 5), (0, 200, 255), -1)
    
    # Title with modern font
    title = "DRIVER DROWSINESS DETECTION SYSTEM"
    cv2.putText(img, title, (25, 45), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, title, (25, 45), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 200, 255), 1)
    
    # Subtitle
    cv2.putText(img, "Real-time Monitoring Active", (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
    
    # Bottom info bar
    info_bar_h = 50
    overlay3 = img.copy()
    cv2.rectangle(overlay3, (0, h - info_bar_h), (w, h), (20, 20, 20), -1)
    cv2.addWeighted(overlay3, 0.85, img, 0.15, 0, img)
    
    # Bottom accent line
    cv2.rectangle(img, (0, h - info_bar_h), (w, h - info_bar_h + 3), (0, 200, 255), -1)
    
    # Status card - bottom left, ABOVE the footer
    card_x = 20
    card_y = h - info_bar_h - 140  # Position it above the footer
    card_w = 200
    card_h = 130
    
    # Draw status card background
    overlay2 = img.copy()
    cv2.rectangle(overlay2, (card_x, card_y), (card_x + card_w, card_y + card_h), (30, 30, 30), -1)
    cv2.addWeighted(overlay2, 0.85, img, 0.15, 0, img)
    
    # Status card border with state-based color
    if eye_state == "OPEN":
        status_color = (0, 255, 100)
        status_text = "EYES OPEN"
        status_bg = (0, 100, 40)
    elif eye_state == "CLOSED":
        status_color = (0, 100, 255)
        status_text = "EYES CLOSED"
        status_bg = (0, 40, 100)
    else:
        status_color = (100, 100, 100)
        status_text = "NO DETECTION"
        status_bg = (40, 40, 40)
    
    cv2.rectangle(img, (card_x, card_y), (card_x + card_w, card_y + card_h), status_color, 2)
    
    # Status badge
    cv2.rectangle(img, (card_x + 8, card_y + 10), (card_x + card_w - 8, card_y + 38), status_bg, -1)
    cv2.rectangle(img, (card_x + 8, card_y + 10), (card_x + card_w - 8, card_y + 38), status_color, 2)
    cv2.putText(img, status_text, (card_x + 25, card_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Metrics section
    metrics_y = card_y + 50
    
    # Eye Aspect Ratio
    cv2.putText(img, "EYE RATIO", (card_x + 15, metrics_y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 180, 180), 1)
    cv2.putText(img, f"{eye_ratio:.3f}", (card_x + 15, metrics_y + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Progress bar for eye ratio
    bar_x = card_x + 15
    bar_y = metrics_y + 25
    bar_w = card_w - 30
    bar_h = 6
    
    # Background bar
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (60, 60, 60), -1)
    
    # Filled bar based on eye ratio
    fill_width = int(min(eye_ratio, 1.0) * bar_w)
    bar_color = (0, 255, 100) if eye_ratio >= 0.15 else (0, 100, 255)
    cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_h), bar_color, -1)
    
    # Closure time
    metrics_y2 = metrics_y + 45
    cv2.putText(img, "CLOSURE TIME", (card_x + 15, metrics_y2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 180, 180), 1)
    
    time_color = (0, 255, 100) if eye_closed_time < 2.0 else (255, 150, 0) if eye_closed_time < 3.0 else (0, 100, 255)
    cv2.putText(img, f"{eye_closed_time:.2f}s", (card_x + 15, metrics_y2 + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, time_color, 1)
    
    # Warning threshold indicator
    threshold_y = metrics_y2 + 25
    cv2.rectangle(img, (bar_x, threshold_y), (bar_x + bar_w, threshold_y + 6), (60, 60, 60), -1)
    threshold_fill = int(min(eye_closed_time / 3.0, 1.0) * bar_w)
    cv2.rectangle(img, (bar_x, threshold_y), (bar_x + threshold_fill, threshold_y + 6), time_color, -1)
    
    # Bottom info bar
    info_bar_h = 50
    
    # Face detection indicator
    face_icon = "👤" if len(faces) > 0 else "⚠"
    face_status = f"Face Detected: {'YES' if len(faces) > 0 else 'NO'}"
    face_color = (0, 255, 100) if len(faces) > 0 else (100, 100, 100)
    
    cv2.putText(img, face_status, (25, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, face_color, 1)
    
    # Instructions
    cv2.putText(img, "Press 'Q' to quit", (w - 200, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
    
    # Alert warning if drowsy
    if eye_closed_time >= 3.0:
        warning_overlay = img.copy()
        cv2.rectangle(warning_overlay, (0, 0), (w, h), (0, 0, 255), 40)
        cv2.addWeighted(warning_overlay, 0.3, img, 0.7, 0, img)
        
        # Pulsing warning text
        pulse = int(abs(np.sin(time.time() * 5) * 255))
        warning_y = h // 2
        cv2.putText(img, "! DROWSINESS ALERT !", (w // 2 - 220, warning_y), 
                    cv2.FONT_HERSHEY_DUPLEX, 1.2, (pulse, pulse, 255), 3)

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Drowsiness threshold
ALERT_SECONDS = 3.0

# Timer
eye_closed_time = 0
prev_time = time.time()

# Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting Driver Drowsiness Detector. Press 'q' to quit.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = frame.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(80,80))
        eye_ratio = 0.0
        eye_state = "NO FACE"

        for (x,y,w,h) in faces:
            face_gray = gray[y:y+h, x:x+w]
            face_color = img[y:y+h, x:x+w]

            # Draw modern face detection box
            cv2.rectangle(img, (x-2, y-2), (x+w+2, y+h+2), (0, 200, 255), 2)
            
            # Corner markers
            corner_len = 20
            cv2.line(img, (x, y), (x + corner_len, y), (0, 255, 100), 3)
            cv2.line(img, (x, y), (x, y + corner_len), (0, 255, 100), 3)
            cv2.line(img, (x + w, y), (x + w - corner_len, y), (0, 255, 100), 3)
            cv2.line(img, (x + w, y), (x + w, y + corner_len), (0, 255, 100), 3)
            cv2.line(img, (x, y + h), (x + corner_len, y + h), (0, 255, 100), 3)
            cv2.line(img, (x, y + h), (x, y + h - corner_len), (0, 255, 100), 3)
            cv2.line(img, (x + w, y + h), (x + w - corner_len, y + h), (0, 255, 100), 3)
            cv2.line(img, (x + w, y + h), (x + w, y + h - corner_len), (0, 255, 100), 3)

            # Eyes detection (upper half)
            upper_half = face_gray[0:int(h/2), :]
            eyes = eye_cascade.detectMultiScale(upper_half, scaleFactor=1.05, minNeighbors=4, minSize=(15,10))

            eye_ratios = []
            for (ex,ey,ew,eh) in eyes:
                # Draw eye rectangles (EXACT original style)
                cv2.rectangle(face_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 1)
                eye_ratios.append(eh / float(ew + 1e-6))

            if eye_ratios:
                eye_ratio = float(np.mean(eye_ratios))
            else:
                eye_ratio = 0.0
            break  # Only first face

        # Eye state logic
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time

        if len(faces) == 0:
            eye_state = "NO FACE"
            eye_closed_time = 0
        else:
            if eye_ratio < 0.15:  # threshold for CLOSED, tune if needed
                eye_state = "CLOSED"
                eye_closed_time += dt
            else:
                eye_state = "OPEN"
                eye_closed_time = 0 # reset timer

        # Alert if eyes closed too long
        if eye_closed_time >= ALERT_SECONDS:
            beep_alert()
            eye_closed_time = 0

        # Draw modern UI
        draw_modern_ui(img, eye_state, eye_ratio, eye_closed_time, faces)

        # Show frame
        cv2.imshow("Driver Drowsiness Detector", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print("Error:", e)

finally:
    cap.release()
    cv2.destroyAllWindows()