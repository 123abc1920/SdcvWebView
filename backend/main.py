from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5200, debug=True)

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4MjMwNjM4MywianRpIjoiYmM5ZmMxOGItNTc0ZC00NDg2LTlhOWQtNzBmM2VkZjMwNGQxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MywibmJmIjoxNzgyMzA2MzgzLCJjc3JmIjoiZDBiZDUxMTgtNGM5NC00YzQ3LWE0MDQtNTdiMjljMWVjYWRiIiwiZXhwIjoxNzgzMTcwMzgzfQ.MlL7DH2orCCFeZcshknBPPzrkrshWHq5oM7mx1De-qw