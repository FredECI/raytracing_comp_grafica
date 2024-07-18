import numpy as np
from PIL import Image

# Classe para definir um vetor 3D
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Adição de vetores
    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    # Subtração de vetores
    def sub(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    # Multiplicação escalar
    def scale(self, s):
        return Vector(self.x * s, self.y * s, self.z * s)

    # Produto escalar (dot product)
    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    # Normalização do vetor
    def normalize(self):
        mag = np.sqrt(self.dot(self))
        return self.scale(1 / mag)

    # Reflexão do vetor
    def reflect(self, normal):
        return self.sub(normal.scale(2 * self.dot(normal)))

# Classe para definir um raio
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()

# Classe para definir uma esfera
class Sphere:
    def __init__(self, center, radius, color, shininess=100):
        self.center = center
        self.radius = radius
        self.color = color
        self.shininess = shininess

    # Interseção do raio com a esfera
    def intersect(self, ray):
        oc = ray.origin.sub(self.center)
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None
        else:
            t = (-b - np.sqrt(discriminant)) / (2.0 * a)
            return t

# Função para traçar os raios e obter a cor do pixel
def trace_ray(ray, spheres, light, depth):
    closest_t = float('inf')
    closest_sphere = None

    for sphere in spheres:
        t = sphere.intersect(ray)
        if t is not None and t < closest_t:
            closest_t = t
            closest_sphere = sphere

    if closest_sphere is not None:
        hit_point = ray.origin.add(ray.direction.scale(closest_t))
        normal = hit_point.sub(closest_sphere.center).normalize()
        to_light = light.sub(hit_point).normalize()
        to_camera = ray.direction.scale(-1)

        # Componente ambiente
        ambient = closest_sphere.color.scale(0.1)

        # Componente difusa
        diff = max(normal.dot(to_light), 0)
        diffuse = closest_sphere.color.scale(diff)

        # Componente especular
        reflection = to_light.reflect(normal)
        spec = max(reflection.dot(to_camera), 0) ** closest_sphere.shininess
        specular = Vector(1, 1, 1).scale(spec)

        color = ambient.add(diffuse).add(specular)

        if depth > 0:
            reflection_dir = ray.direction.reflect(normal)
            reflected_ray = Ray(hit_point, reflection_dir)
            reflected_color = trace_ray(reflected_ray, spheres, light, depth - 1)
            color = color.scale(0.8).add(reflected_color.scale(0.2))

        return color

    return Vector(0, 0, 0)

# Função principal para gerar a imagem
def render(width, height, spheres, light):
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    camera = Vector(0, 0, 1)

    for y in range(height):
        for x in range(width):
            u = (x / width) * 2 - 1
            v = (y / height) * 2 - 1
            ray_direction = Vector(u, v, -1).sub(camera).normalize()
            ray = Ray(camera, ray_direction)
            color = trace_ray(ray, spheres, light, 1)
            pixels[x, y] = (
                min(int(color.x * 255), 255),
                min(int(color.y * 255), 255),
                min(int(color.z * 255), 255)
            )

    return image

# Exemplo de uso com iluminação
spheres = [
    Sphere(Vector(0, 0, -3), 1, Vector(1, 0, 0)),  # Esfera vermelha
    Sphere(Vector(2, 0, -4), 1, Vector(0, 1, 0)),  # Esfera verde
    Sphere(Vector(-2, 0, -4), 1, Vector(0, 0, 1)),  # Esfera azul
    Sphere(Vector(0, -1001, -3), 1000, Vector(1, 1, 0))  # Plano amarelo
]

light = Vector(5, 5, -10)
width, height = 400, 300  # Reduzir a resolução ainda mais para acelerar o processo
image = render(width, height, spheres, light)
image.save('ray_tracing_espheres.png')
