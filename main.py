import os
from dotenv import load_dotenv
from fastapi import FastAPI
from PIL import Image
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse

app = FastAPI()

load_dotenv()

MAIN_PATH = os.environ.get('MAIN_PATH')


@app.get('/resize')
async def resizing(filename: str, width: int = None, height: int = None):
    path = os.path.join(MAIN_PATH, filename)

    if not os.path.exists(path):
        raise HTTPException(detail='Файл не найден',
                            status_code=status.HTTP_400_BAD_REQUEST)

    if (width is None) or (height is None):
        return FileResponse(path=path, filename=f'{filename}',
                            media_type='multipart/form-data')

    filename_with_parameters = f'{filename.split(".")[0]}_{width}x{height}.{filename.split(".")[1]}'
    alternative_path = os.path.join(MAIN_PATH, filename_with_parameters)
    if os.path.exists(alternative_path):
        return FileResponse(path=alternative_path, filename=f'{filename_with_parameters}',
                            media_type='multipart/form-data')

    img = Image.open(path)
    width_img, height_img = img.size  # width - ширина, height - высота

    if width_img > height_img:
        ratio = width_img / width
        new_height = int(height_img / ratio)
        new_image = img.resize((width, new_height))
    else:
        ratio = height_img / height
        new_width = int(width_img / ratio)
        new_image = img.resize((new_width, height))

    new_image.save(alternative_path)
    return FileResponse(path=alternative_path, filename=f'{filename_with_parameters}',
                        media_type='multipart/form-data')
