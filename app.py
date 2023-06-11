from flask import Flask, render_template,Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)

@app.route("/")
def index():
    return render_template('index.html')

def generate_frames():

    while True:
        #read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            _, buffr = cv2.imencode('.jpg', frame)
            frame = buffr.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
