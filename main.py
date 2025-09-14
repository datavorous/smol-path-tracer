from core.camera import Camera
from core.vec import Vec3, Color
from core.hits import HittableList
from core.utils import ray_color, write_color
from core.ray import Ray
from shapes.sphere import Sphere
from shapes.quad import Quad
from shapes.material import Lambertian, EmissiveMaterial, Metal

import random


def main():
    aspect_ratio = 16.0 / 9.0
    image_width = 1600
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 100
    max_depth = 6
    world = HittableList()
    pixels = []

    def make_cube(center: Vec3, size: float, material):
        hs = size / 2.0
        world.add(
            Quad(
                Vec3(center.x - hs, center.y - hs, center.z + hs),
                Vec3(center.x + hs, center.y - hs, center.z + hs),
                Vec3(center.x + hs, center.y + hs, center.z + hs),
                Vec3(center.x - hs, center.y + hs, center.z + hs),
                material,
            )
        )

        world.add(
            Quad(
                Vec3(center.x + hs, center.y - hs, center.z - hs),
                Vec3(center.x - hs, center.y - hs, center.z - hs),
                Vec3(center.x - hs, center.y + hs, center.z - hs),
                Vec3(center.x + hs, center.y + hs, center.z - hs),
                material,
            )
        )

        world.add(
            Quad(
                Vec3(center.x - hs, center.y - hs, center.z - hs),
                Vec3(center.x - hs, center.y - hs, center.z + hs),
                Vec3(center.x - hs, center.y + hs, center.z + hs),
                Vec3(center.x - hs, center.y + hs, center.z - hs),
                material,
            )
        )
        world.add(
            Quad(
                Vec3(center.x + hs, center.y - hs, center.z + hs),
                Vec3(center.x + hs, center.y - hs, center.z - hs),
                Vec3(center.x + hs, center.y + hs, center.z - hs),
                Vec3(center.x + hs, center.y + hs, center.z + hs),
                material,
            )
        )
        world.add(
            Quad(
                Vec3(center.x - hs, center.y + hs, center.z + hs),
                Vec3(center.x + hs, center.y + hs, center.z + hs),
                Vec3(center.x + hs, center.y + hs, center.z - hs),
                Vec3(center.x - hs, center.y + hs, center.z - hs),
                material,
            )
        )
        world.add(
            Quad(
                Vec3(center.x - hs, center.y - hs, center.z - hs),
                Vec3(center.x + hs, center.y - hs, center.z - hs),
                Vec3(center.x + hs, center.y - hs, center.z + hs),
                Vec3(center.x - hs, center.y - hs, center.z + hs),
                material,
            )
        )

    world.add(Sphere(Vec3(0, 0, 0), 0.3, EmissiveMaterial(Color(1.0, 0.8, 0.6), 10)))

    make_cube(Vec3(0, 0, 2), 0.8, Lambertian(Color(0.7, 0.3, 0.3)))
    make_cube(Vec3(0, 0, -2), 0.8, Metal(Color(0.8, 0.8, 0.9), 0.1))
    make_cube(Vec3(-2, 0, 0), 0.8, Lambertian(Color(0.3, 0.7, 0.3)))
    make_cube(Vec3(2, 0, 0), 0.8, Metal(Color(0.9, 0.7, 0.3), 0.2))

    world.add(Sphere(Vec3(-1.5, 0, 1.5), 0.5, Lambertian(Color(0.2, 0.2, 0.8))))
    world.add(Sphere(Vec3(1.5, 0, 1.5), 0.5, Metal(Color(0.8, 0.2, 0.8), 0.3)))
    world.add(Sphere(Vec3(1.5, 0, -1.5), 0.5, Lambertian(Color(0.8, 0.8, 0.2))))
    world.add(Sphere(Vec3(-1.5, 0, -1.5), 0.5, Metal(Color(0.3, 0.8, 0.8), 0.1)))

    world.add(Sphere(Vec3(0, -100.5, 0), 100, Lambertian(Color(0.2, 0.2, 0.2))))

    """
    TODO: write about camera, and paste a few diagrams
    this part was very confusing for me
    """
    camera = Camera(
        Vec3(4, 3, 4),
        Vec3(0, 0, 0),
        Vec3(0, 1, 0),
        40,
        aspect_ratio,
    )

    print(
        f"Starting render: {image_width}x{image_height}, {samples_per_pixel} samples per pixel"
    )
    print(f"Total pixels: {image_width * image_height}")
    total_pixels = image_width * image_height
    done = 0

    # the main work starts exactly here:
    for j in range(image_height - 1, -1, -1):
        # we go from top to bottom
        # scan each horizontal row of pixels
        # and take actions accordingly

        for i in range(image_width):
            pixel_color = Color(0, 0, 0)
            # everything is assigned a base color
            # then we shoot multiple rays from our camera
            # to perform anti aliasing

            for _ in range(samples_per_pixel):
                # u, v are discrete increments for: left-right and top-bottom
                u = (i + random.random()) / (image_width - 1)
                v = (j + random.random()) / (image_height - 1)
                # shoot some rays

                # returns a ray object, ray object has the origin, and a P(t) ray equation
                ray = camera.get_ray(u, v)
                # and we try to change the color

                """
                so important:
                ray color has a HitList in it
                first we check if there we have exceeded the depth limit or not
                depth limit here refers to the number of times the ray can bounce off from a surface
                the 'world' param (a HittableList has already provided the entities to check collisions with)

                """
                pixel_color = pixel_color + ray_color(ray, world, max_depth)
                # so after lots of magic done per ray, withing the ray_color() function
                # , we get the color we need for a given pixel
                # the ray color is techincally the heart of this path tracer
            done += 1
            if done % 1000 == 0:
                percent = done / total_pixels * 100
                print(f"{percent:.2f}% done", end="\r", flush=True)

            rgb = write_color(pixel_color, samples_per_pixel)
            pixels.append(rgb)

    with open("output/image.ppm", "wb") as f:
        f.write(f"P6\n{image_width} {image_height}\n255\n".encode())
        for r, g, b in pixels:
            f.write(bytes([r, g, b]))
    print("Saved as 'output/image.ppm'")


main()
