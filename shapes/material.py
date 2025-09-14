from core.vec import random_unit_vector
from core.ray import Ray
from core.utils import *


class Material:
    def scatter(self, ray_in, hit_record):
        pass

    def emitted(self):
        return Color(0, 0, 0)


class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo
        # albedo means surface color (how much the light it reflects)

    def scatter(self, ray_in, hit_record):
        # pick a random direction biased around the normal -> diffuse reflection
        scatter_direction = hit_record.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        scattered_ray = Ray(hit_record.p, scatter_direction)
        # THE COLOR FADES according to SURFACE COLOR
        attenuation = self.albedo

        # the true here refers to the fact that diffuse materials never absorb
        return True, scattered_ray, attenuation


class EmissiveMaterial(Material):
    def __init__(self, emit_color, brightness=1.0):

        # base light color, and intensity multiplier
        self.emit_color = emit_color
        self.brightness = brightness

    def scatter(self, ray_in, hit_record):
        # light sources DONT scatter, they just emit peacefully
        return False, None, Color(0, 0, 0)

    def emitted(self):
        # emits colored light into the scene
        return self.emit_color * self.brightness


class Metal(Material):
    def __init__(self, albedo, fuzziness=0.0):
        self.albedo = albedo
        # fuzziness determines the Blurryness
        # 0 -> perfect mirror, 1 -> very rough
        self.fuzziness = min(fuzziness, 1.0)

    def scatter(self, ray_in, hit_record):
        reflected = reflect(ray_in.direction.unit_vector(), hit_record.normal)

        # computes mirror reflection of incoming ray direction around the normal, adds randomness to blurry reflections -->> spawn reflected ray at the hit point
        if self.fuzziness > 0:
            reflected = reflected + self.fuzziness * random_unit_vector()

        scattered_ray = Ray(hit_record.p, reflected)
        attenuation = self.albedo
        scattered = (
            scattered_ray.direction.dot(hit_record.normal) > 0
        )  # i kind of like this inline thing
        return scattered, scattered_ray, attenuation


# TODO: dielectrics ughh
