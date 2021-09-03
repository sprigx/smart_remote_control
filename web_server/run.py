from urls import app
import uvicorn

def main():
    uvicorn.run('controllers:app', port=8000, reload=True)

if __name__ == '__main__':
    main()
