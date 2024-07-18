import numpy as np
import matplotlib.pyplot as plt

# Função para normalizar um vetor
def normalize(vector):
    return vector / np.linalg.norm(vector)

# Função para calcular a reflexão de um vetor em relação a um eixo
def reflect(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

# Função para verificar interseção do raio com um plano
def intersect_plane(point, normal, ray_origin, ray_dir):
    denom = np.dot(ray_dir, normal)
    if np.abs(denom) > 1e-6:  # Verifica se o denominador não é zero
        t = np.dot(point - ray_origin, normal) / denom
        if t >= 0:
            return t
    return None

# Função para verificar interseção do raio com uma esfera
def intersect_sphere(center, radius, ray_origin, ray_dir):
    b = 2 * np.dot(ray_dir, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None

# Função para encontrar o objeto mais próximo intersectado pelo raio
def find_closest_object(objects, ray_origin, ray_dir):
    distances = []
    for obj in objects:
        if obj['type'] == 'sphere':
            distances.append(intersect_sphere(obj['center'], obj['radius'], ray_origin, ray_dir))
        elif obj['type'] == 'plane':
            distances.append(intersect_plane(obj['point'], obj['normal'], ray_origin, ray_dir))
    
    closest_object = None
    min_distance = np.inf
    for idx, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            closest_object = objects[idx]
    return closest_object, min_distance

# Função principal de ray tracing
def trace_ray(ray_origin, ray_dir, objects, light, camera, depth=0, max_depth=3):
    # Verifica se a profundidade máxima de recursão foi atingida
    if depth >= max_depth:
        return np.zeros((3))
    
    # Encontra o objeto mais próximo que o raio intersecta
    closest_object, min_distance = find_closest_object(objects, ray_origin, ray_dir)
    if closest_object is None:
        return np.zeros((3))  # Retorna preto se não houver interseção

    intersection = ray_origin + min_distance * ray_dir
    if closest_object['type'] == 'sphere':
        surface_normal = normalize(intersection - closest_object['center'])
    elif closest_object['type'] == 'plane':
        surface_normal = closest_object['normal']
    
    shifted_point = intersection + 1e-5 * surface_normal
    to_light = normalize(light['position'] - shifted_point)

    _, min_distance = find_closest_object(objects, shifted_point, to_light)
    light_distance = np.linalg.norm(light['position'] - intersection)
    is_shadowed = min_distance < light_distance

    if is_shadowed:
        return np.zeros((3))  # Retorna preto se estiver sombreado

    illumination = np.zeros((3))

    # Componente ambiente
    illumination += closest_object['ambient'] * light['ambient']
    # Componente difusa
    illumination += closest_object['diffuse'] * light['diffuse'] * np.dot(to_light, surface_normal)
    # Componente especular
    to_camera = normalize(camera - intersection)
    H = normalize(to_light + to_camera)
    illumination += closest_object['specular'] * light['specular'] * np.dot(surface_normal, H) ** (closest_object['shininess'] / 4)

    # Reflexão
    if 'reflection' in closest_object:
        reflection_dir = reflect(ray_dir, surface_normal)
        reflection = closest_object['reflection'] * trace_ray(shifted_point, reflection_dir, objects, light, camera, depth + 1, max_depth)
        illumination += reflection

    return illumination

# Parâmetros da imagem
width = 1920
height = 1080
camera = np.array([0, 0, 1])
aspect_ratio = float(width) / height
screen = (-1, 1 / aspect_ratio, 1, -1 / aspect_ratio)

light = {
    'position': np.array([0, 5, 5]),
    'ambient': np.array([1, 1, 1]),
    'diffuse': np.array([1, 1, 1]),
    'specular': np.array([1, 1, 1])
}

objects = [
    {'type': 'sphere', 'center': np.array([-0.3, 0.6, -0.6]), 'radius': 0.09, 'ambient': np.array([0.2, 0.3, 0.2]), 'diffuse': np.array([0.6, 0.8, 0.2]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'type': 'sphere', 'center': np.array([-0.7, -0.1, -0.4]), 'radius': 0.20, 'ambient': np.array([0.2, 0.3, 0.2]), 'diffuse': np.array([0.6, 0.8, 0.2]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'type': 'sphere', 'center': np.array([0.4, -0.3, -0.5]), 'radius': 0.15, 'ambient': np.array([0.2, 0.3, 0.2]), 'diffuse': np.array([0.6, 0.8, 0.2]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'type': 'sphere', 'center': np.array([0, 0.1, -1]), 'radius': 0.55, 'ambient': np.array([0.3, 0.1, 0.1]), 'diffuse': np.array([0.8, 0.2, 0.2]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5},
    {'type': 'plane', 'point': np.array([0, -0.5, 0]), 'normal': np.array([0, 1, 0]), 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.6, 0.5, 0.7]), 'specular': np.array([0.5, 0.5, 0.5]), 'shininess': 50}
]

# Renderiza a imagem
image = np.zeros((height, width, 3))
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)
        color = trace_ray(origin, direction, objects, light, camera)
        image[i, j] = np.clip(color, 0, 1)

plt.imsave('ray_tracing_espheres.png', image)
