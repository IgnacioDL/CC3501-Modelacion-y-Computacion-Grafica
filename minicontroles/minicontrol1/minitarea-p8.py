# Ignacio Díaz Lara
import scene_graph as sg
import basic_shapes as bs
import transformations as tr
import easy_shaders as es
import complex_shapes as cs
import other_shaders as os


# asumo que existen complex_shapes y other_shaders para los poligonos
# que describí anteriormente y triángulos

def create_scene():
    gpu_cuchillo = os.toGPUShape(bs.createColorCuchillo(1, 1, 0))
    gpu_green_triangle = os.toGPUShape(bs.createColorTriangle(0, 1, 0))
    gpu_yellow_triangle = os.toGPUShape(bs.createColorTriangle(1, 1, 0))
    gpu_green_quad = es.toGPUShape(bs.createColorQuad(1, 1, 0))
    gpu_yellow_quad = es.toGPUShape(bs.createColorQuad(0, 1, 0))
    gpu_yellow_d = es.toGPUShape(bs.createColorD(0, 1, 0))

    # El cuchillo
    cuchillo = sg.SceneGraphNode('cuchillo')
    cuchillo.transform = tr.matmul([tr.translate(-8 / 15, -1 / 22, 0), tr.scale(3, 3, 1), tr.rotationZ(180)])
    cuchillo.childs += [gpu_cuchillo]

    # La mesa
    mc1 = sg.SceneGraphNode('mc1')
    mc1.transform = tr.scale(4, 4, 1)
    mc1.childs += [gpu_yellow_quad]

    mt1 = sg.SceneGraphNode('mt1')
    mt1.transform = tr.translate(-1 / 15, -3 / 22, 0)
    mt1.childs += [gpu_yellow_quad]

    mt2 = sg.SceneGraphNode('mt2')
    mt2.transform = tr.translate(1 / 15, -3 / 22, 0)
    mt2.childs += [gpu_yellow_quad]

    MesaT = sg.SceneGraphNode('MesaT')
    MesaT.childs += [mt1, mt2]
    MesaT.transform = tr.scale(2, 2, 1)

    Mesa = sg.SceneGraphNode('Mesa')
    Mesa.childs += [MesaT, mc1]
    Mesa.transform = tr.matmul([tr.translate(5 / 15, 8 / 22, 0), tr.scale(2, 1.5, 1), tr.rotationZ(180)])

    # El Árbol
    ac1 = sg.SceneGraphNode('ac1')
    ac1.transform = tr.scale(2, 2, 1)
    ac1.childs += [gpu_green_quad]

    at1 = sg.SceneGraphNode('at1')
    at1.transform = tr.translate(-1 / 15, 0, 0)
    at1.childs += [gpu_green_triangle]

    at2 = sg.SceneGraphNode('at2')
    at2.transform = tr.translate(1 / 15, 0, 0)
    at2.childs += [gpu_green_triangle]

    Rama1 = sg.SceneGraphNode('Rama1')
    Rama1.childs += [at1, at2]
    Rama1.transform = tr.translate(0, 4 / 22, 0)

    at3 = sg.SceneGraphNode('at3')
    at3.transform = tr.translate(-1 / 15, 0, 0)
    at3.childs += [gpu_green_triangle]

    at4 = sg.SceneGraphNode('at4')
    at4.transform = tr.translate(1 / 15, 0, 0)
    at4.childs += [gpu_green_triangle]

    Rama2 = sg.SceneGraphNode('Rama2')
    Rama2.childs += [at3, at4]
    Rama2.transform = tr.translate(0, 2 / 22, 0)

    ArbolT = sg.SceneGraphNode('ArbolT')
    ArbolT.childs += [Rama1, Rama2]
    ArbolT.transform = tr.scale(2, 2, 1)

    Arbol = sg.SceneGraphNode('Arbol')
    Arbol.childs += [ArbolT, ac1]
    Arbol.transform = tr.matmul([tr.translate(6 / 15, -13 / 22, 0), tr.scale(4, 2, 1), tr.rotationZ(360)])

    # La Firma

    d = sg.SceneGraphNode('d')
    d.transform = tr.translate(7 / 22, 0, 0)
    d.childs += [gpu_yellow_d]

    i1 = sg.SceneGraphNode('i1')
    i1.transform = tr.matmul([tr.translate(-1 / 15, 3.5 / 22, 0), tr.scale(1, 6, 1)])
    i1.childs += [gpu_green_quad]

    i2 = sg.SceneGraphNode('i2')
    i2.transform = tr.matmul([tr.translate(-1 / 15, 0.5 / 22, 0), tr.scale(2, 5, 1)])
    i2.childs += [gpu_green_quad]

    i3 = sg.SceneGraphNode('i3')
    i3.transform = tr.matmul([tr.translate(-1 / 15, -2.5 / 22, 0), tr.scale(1, 6, 1)])
    i3.childs += [gpu_green_quad]

    i = sg.SceneGraphNode('i')
    i.childs += [i1, i2, i3]

    Firma = sg.SceneGraphNode('Firma')
    Firma.childs += [i, d]
    Firma.transform = tr.matmul([tr.translate(-10 / 15, 19 / 22, 0)])

    # El Cepillo de Dientes

    ct1 = sg.SceneGraphNode('ct1')
    ct1.transform = tr.translate(0, 1 / 22, 0)
    ct1.childs += [gpu_green_triangle]

    ct2 = sg.SceneGraphNode('ct2')
    ct2.transform = tr.translate(0, 3 / 22, 0)
    ct2.childs += [gpu_green_triangle]

    ct3 = sg.SceneGraphNode('ct3')
    ct3.transform = tr.translate(0, 5 / 22, 0)
    ct3.childs += [gpu_green_triangle]

    CepilloT = sg.SceneGraphNode('CepilloT')
    CepilloT.childs += [ct1, ct2, ct3]
    CepilloT.transform = tr.matmul([tr.translate(-3 / 15, 0, 0), tr.scale(2, 2, 1)])

    cc1 = sg.SceneGraphNode('cc1')
    cc1.transform = tr.translate(0, 5 / 22, 0)
    cc1.childs += [gpu_green_quad]

    cc2 = sg.SceneGraphNode('cc2')
    cc2.transform = tr.translate(0, 3 / 22, 0)
    cc2.childs += [gpu_green_quad]

    cc3 = sg.SceneGraphNode('cc3')
    cc3.transform = tr.translate(0, 1 / 22, 0)
    cc3.childs += [gpu_green_quad]

    cc4 = sg.SceneGraphNode('cc4')
    cc4.transform = tr.translate(0, -1 / 22, 0)
    cc4.childs += [gpu_green_quad]

    cc5 = sg.SceneGraphNode('cc5')
    cc5.transform = tr.translate(0, -3 / 22, 0)
    cc5.childs += [gpu_green_quad]

    cc6 = sg.SceneGraphNode('cc6')
    cc6.transform = tr.translate(0, -5 / 22, 0)
    cc6.childs += [gpu_green_quad]

    CepilloC = sg.SceneGraphNode('CepilloC')
    CepilloC.childs += [ct1, ct2, ct3]
    CepilloC.transform = tr.matmul([tr.translate(-1 / 15, 0, 0), tr.scale(2, 2, 1)])

    Cepillo = sg.SceneGraphNode('Cepillo')
    Cepillo.childs += [CepilloT, CepilloC]
    Cepillo.transform = tr.matmul([tr.translate(2 / 15, -20 / 22, 0), tr.scale(0.5, 1.5, 1), tr.rotationZ(90)])

    # el Mundo
    mundo = sg.SceneGraphNode('mundo')
    mundo.childs += [Mesa, Arbol, Cepillo, cuchillo, Firma]

    return mundo
