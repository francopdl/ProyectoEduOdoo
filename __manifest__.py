{
    'name': 'Gestión de Academia',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Módulo para gestionar cursos, alumnos, profesores y sesiones',
    'description': """
        Gestión completa de academia con:
        - Cursos con niveles (A1, A2, B1, B2, C1, C2)
        - Profesores y sus asignaciones
        - Alumnos inscritos
        - Sesiones y clases
        - Facturación de matrículas
    """,
    'author': 'Academia Team',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/curso_views.xml',
        'views/profesor_views.xml',
        'views/alumno_views.xml',
        'views/sesion_views.xml',
        'views/clase_views.xml',
        'views/facturacion_views.xml',
        'views/matricula_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
