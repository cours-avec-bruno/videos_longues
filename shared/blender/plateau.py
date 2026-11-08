"""Le « plateau » des tableaux de la vie de Manoj (Blender, Eevee) : la grammaire visuelle validée par Bruno en S06.

Un grand sol sombre et brillant (les reflets), un monde presque noir avec une brume légère (les faisceaux),
des socles ronds, des projecteurs, des mannequins sans visage (mannequin.py) : Manoj en rouge, les autres en argile.

    import sys; sys.path.append(".../shared/blender")
    import plateau as P
    sc = P.scene(test=False, fps=24, images=120)
    M = P.materiaux()
    P.sol()
    P.estrade("ecole", (0, 0), 1.6, M["terre"])
    P.perso("manoj", pose, 0.55, True, M["rouge"], (0, 0, P.H), 0)
"""
import math

import bpy
from mathutils import Vector

from mannequin import mannequin

rad = math.radians
H = 0.05                    # dessus d'un socle


def scene(test=False, fps=24, images=1, largeur=1920, hauteur=1080):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.fps = fps
    sc.frame_start, sc.frame_end = 1, max(1, images)
    sc.render.resolution_x, sc.render.resolution_y = (960, 540) if test else (largeur, hauteur)
    ee = sc.eevee
    for attr, val in (("use_raytracing", True), ("taa_render_samples", 64), ("use_shadows", True),
                      ("volumetric_tile_size", "8"), ("volumetric_samples", 64), ("use_volumetric_shadows", True)):
        try:
            setattr(ee, attr, val)
        except Exception as e:
            print("[plateau] réglage ignoré", attr, e)
    try:
        ee.ray_tracing_options.resolution_scale = "1"
    except Exception:
        pass
    sc.render.use_motion_blur = True
    try:
        sc.render.motion_blur_shutter = 0.6
    except Exception:
        pass
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    w = bpy.data.worlds.new("monde")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes["Background"].inputs[0].default_value = (0.0025, 0.0028, 0.0035, 1)
    vol = nt.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Density"].default_value = 0.012
    vol.inputs["Anisotropy"].default_value = 0.55
    nt.links.new(vol.outputs[0], nt.nodes["World Output"].inputs["Volume"])
    return sc


def materiau(nom, couleur, rugosite=0.55, brillance=0.35, metal=0.0):
    m = bpy.data.materials.get(nom) or bpy.data.materials.new(nom)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*couleur, 1)
    b.inputs["Roughness"].default_value = rugosite
    b.inputs["Metallic"].default_value = metal
    for cle in ("Specular IOR Level", "Specular"):
        if cle in b.inputs:
            b.inputs[cle].default_value = brillance
    return m


def materiaux():
    return {
        "rouge": materiau("manoj", (0.62, 0.07, 0.035), 0.5, 0.45),
        "argile": materiau("argile", (0.42, 0.40, 0.37), 0.62, 0.3),
        "argile_v": materiau("argile_vieille", (0.36, 0.345, 0.33), 0.7, 0.25),
        "argile_s": materiau("argile_sombre", (0.25, 0.24, 0.23), 0.65, 0.3),
        "sol": materiau("sol", (0.018, 0.018, 0.02), 0.16, 0.6),
        "terre": materiau("terre", (0.16, 0.10, 0.06), 0.9, 0.2),
        "terre_seche": materiau("terre_seche", (0.30, 0.20, 0.12), 0.92, 0.15),
        "bois": materiau("bois", (0.22, 0.13, 0.07), 0.6, 0.3),
        "bois_clair": materiau("bois_clair", (0.42, 0.28, 0.15), 0.55, 0.3),
        "glaise": materiau("glaise", (0.34, 0.19, 0.10), 0.85, 0.2),
        "chaux": materiau("chaux", (0.55, 0.52, 0.46), 0.85, 0.2),
        "tableau_noir": materiau("tableau_noir", (0.03, 0.05, 0.04), 0.7, 0.2),
        "fonte": materiau("fonte", (0.03, 0.03, 0.03), 0.35, 0.6),
        "inox": materiau("inox", (0.8, 0.8, 0.8), 0.18, 0.5, metal=1.0),
        "laiton": materiau("laiton", (0.75, 0.52, 0.22), 0.28, 0.5, metal=1.0),
        "linge": materiau("linge", (0.82, 0.80, 0.76), 0.9, 0.15),
        "souci": materiau("souci", (0.95, 0.42, 0.03), 0.7, 0.2),
        "billet": materiau("billet", (0.55, 0.50, 0.42), 0.8, 0.2),
        "bambou": materiau("bambou", (0.45, 0.36, 0.18), 0.6, 0.3),
    }


def emission(nom, couleur, force):
    m = bpy.data.materials.new(nom)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.remove(n["Principled BSDF"])
    e = n.new("ShaderNodeEmission")
    e.inputs[0].default_value = (*couleur, 1)
    e.inputs[1].default_value = force
    m.node_tree.links.new(e.outputs[0], n["Material Output"].inputs[0])
    return m, e


def boite(nom, dims, pos, mat, rot=(0, 0, 0), biseau=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos, rotation=[rad(a) for a in rot])
    o = bpy.context.object
    o.name = nom
    o.scale = dims
    bpy.ops.object.transform_apply(scale=True)
    if biseau:
        b = o.modifiers.new("biseau", "BEVEL")
        b.width, b.segments = biseau, 2
    o.data.materials.append(mat)
    return o


def cylindre(nom, r, h, pos, mat, rot=(0, 0, 0), sommets=32, echelle=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=sommets, radius=r, depth=h, location=pos, rotation=[rad(a) for a in rot])
    o = bpy.context.object
    o.name = nom
    o.scale = echelle
    o.data.materials.append(mat)
    return o


def sphere(nom, r, pos, mat, echelle=(1, 1, 1), sub=2):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=r, location=pos)
    o = bpy.context.object
    o.name = nom
    o.scale = echelle
    o.data.materials.append(mat)
    return o


def perso(nom, pose, ech, enfant, mat, pos, angle, au_sol=True):
    o = mannequin(nom, pose, echelle=ech, enfant=enfant, mat=mat, au_sol=au_sol)
    o.location = pos
    o.rotation_euler.z = rad(angle)       # 0 : il regarde vers -Y ; 90 : vers +X ; -90 : vers -X
    return o


def projecteur(nom, pos, vise, energie, couleur=(1.0, 0.9, 0.78), angle=38, flou=0.35, rayon=0.25):
    bpy.ops.object.light_add(type="SPOT", location=pos)
    L = bpy.context.object
    L.name = nom
    L.data.energy = energie
    L.data.color = couleur
    L.data.spot_size = rad(angle)
    L.data.spot_blend = flou
    L.data.shadow_soft_size = rayon
    L.rotation_euler = (Vector(vise) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
    return L


def lampe(nom, pos, energie, couleur, rayon=0.05, type_="POINT"):
    bpy.ops.object.light_add(type=type_, location=pos)
    L = bpy.context.object
    L.name = nom
    L.data.energy = energie
    L.data.color = couleur
    L.data.shadow_soft_size = rayon
    return L


def estrade(nom, xy, rayon, mat):
    """Le socle d'une scène : un disque bas, posé sur le sol brillant."""
    o = cylindre(f"socle_{nom}", rayon, 0.05, (xy[0], xy[1], 0.025), mat, sommets=96)
    b = o.modifiers.new("biseau", "BEVEL")
    b.width, b.segments = 0.012, 2
    return o


def sol(centre=(0, 0), taille=(200, 80)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(centre[0], centre[1], 0))
    s = bpy.context.object
    s.scale = (*taille, 1)
    s.data.materials.append(bpy.data.materials["sol"])
    return s


def viser(depuis, vers):
    return (Vector(vers) - Vector(depuis)).to_track_quat("-Z", "Y").to_euler()
