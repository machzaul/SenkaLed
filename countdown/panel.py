from rgbmatrix import RGBMatrix, RGBMatrixOptions
def create_panel():
    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "regular"
    options.gpio_slowdown = 2
    options.drop_privileges = False
    matrix = RGBMatrix(options=options)
    return matrix
