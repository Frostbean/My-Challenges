from PIL import Image
import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data('NCtfU{Y0u_h4v3_f0und_7h3_53cr37_1n_7h3_l060!}')
qr.make(fit=True)

qr_img = qr.make_image(fill='black', back_color='white')
qr_img = qr_img.convert("1")
qr_img = qr_img.resize((720, 720))

# 打开目标图像
img = Image.open("logo.png").convert("RGBA")

# 将二维码隐藏到目标图像的 alpha 通道的最低有效位
pixels = img.load()
qr_pixels = qr_img.load()

for y in range(img.height):
    for x in range(img.width):
        r, g, b, a = pixels[x, y]
        qr_pixel = qr_pixels[x, y]

        new_a = (a & 0xFE) | (1 if qr_pixel == 0 else 0)

        pixels[x, y] = (r, g, b, new_a)

qr_img.save("qr_code.png")
img.save("challenge.png")
