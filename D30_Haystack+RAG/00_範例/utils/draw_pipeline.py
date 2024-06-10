# 導入需要的函數和模組
from IPython.display import Image, display  # 用於顯示圖片的 IPython 函數


# 定義擴展的 draw 函數
def draw_and_display(pipeline, image_path):
    """
    擴展 draw 函數，生成圖片後直接在 Jupyter Notebook 中顯示。

    :param pipeline: 要繪製的管道對象
    :param image_path: 保存圖片的路徑
    """
    # 生成並保存管道圖片
    pipeline.draw(image_path)

    # 讀取並顯示圖片
    display(Image(filename=image_path))
