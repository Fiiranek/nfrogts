from PIL import Image

from models.frog import Frog

SIZE = 854


def generate_frog_img(frog: Frog):
    body_img = Image.open(f'img/body/{frog.body}.png')
    for gadget in frog.gadgets:
        gadget_img = Image.open(f'img/gadgets/{gadget}.png')
        body_img.paste(gadget_img, (0, 0), gadget_img)
    body_img.save(f'img/frogs/{frog.name}.png')


if __name__ == '__main__':
    for i in range(5000):
        generate_frog_img(Frog(i))
