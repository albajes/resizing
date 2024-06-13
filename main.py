import io
from fastapi import FastAPI, UploadFile
from PIL import Image, UnidentifiedImageError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import StreamingResponse

app = FastAPI()


@app.post('/resize')
async def resizing(width: int, height: int, picture: UploadFile):
    try:
        img = Image.open(picture.file)
    except UnidentifiedImageError:
        raise HTTPException(detail='Неподдерживаемый формат изображения',
                            status_code=status.HTTP_400_BAD_REQUEST)

    width_img, height_img = img.size  # width - ширина, height - высота

    if width_img > height_img:
        ratio = width_img / width
        new_height = int(height_img / ratio)
        new_image = img.resize((width, new_height))
    else:
        ratio = height_img / height
        new_width = int(width_img / ratio)
        new_image = img.resize((new_width, height))

    buff = io.BytesIO()
    new_image.save(buff, format='PNG')
    buff.seek(0)
    return StreamingResponse(buff, headers={'Content-Disposition': 'attachment; filename="picture.png"'})