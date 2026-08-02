from app.detection.predictor import predictor

results = predictor.predict("images/me.jpg")

for result in results:
    result.show()