from visdom import Visdom
import numpy as np
import logging

logging.basicConfig()

viz = Visdom()
assert viz.check_connection()

viz.images(
    np.random.randn(20, 3, 64, 64),
    opts=dict(title='Random images', caption='How random.')
)