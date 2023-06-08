import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

class ScaledFigure(plt.Figure):
    UNITS = {
        'mm': 1/25.4,
        'cm': 1/2.54,
        'in': 1,
    }

    def _scaled(self, p, normalized=False):
        if normalized:
            return [pp * self.sf_norm_scale[i%2] for i, pp in enumerate(p)]
        else:
            return [pp * self.sf_scale for pp in p]

    def __init__(self, figsize, units='mm', label_offset=None, label_params={}, **kwargs):
        self.sf_units = units
        self.sf_figsize = figsize
        self.sf_scale = self.UNITS[units]
        self.sf_norm_scale =  (1 / figsize[0], 1 / figsize[1])

        self.label_params = dict(va='top', ha='left', fontweight='bold')
        self.label_params.update(label_params)

        if label_offset is None:
            self.label_offset = 1.5/25.4 / self.sf_scale
        else:
            self.label_offest = label_offset

        super().__init__(figsize=self._scaled(figsize), **kwargs)

    def add_axes(self, rect, label=None, label_params={}, *args, **kwargs):
        ax = super().add_axes(self._scaled(rect, True), *args, **kwargs)

        lp = self.label_params.copy()
        lp.update(label_params)

        if label:
            ax.text(float(self.label_offset)/rect[2], 1-float(self.label_offset)/rect[3], label, transform=ax.transAxes, **lp)

        return ax

    def whole_figure_axes(self, *args, **kwargs):
        ax = super().add_axes([0, 0, 1, 1], *args, **kwargs)
        ax.set_xlim(0, self.sf_figsize[0])
        ax.set_ylim(0, self.sf_figsize[1])
        ax.set_axis_off()
        return ax

    def as_image(self, **kwargs):
        buffer = io.BytesIO()
        self.savefig(buffer, format='png', **kwargs)
        return Image.open(buffer)

    def as_svg(self, **kwargs):
        buffer = io.BytesIO()
        self.savefig(buffer, format='svg', **kwargs)
        buffer.seek(0)
        return buffer.read()

    def add_image(self, rect, img, label=None, ha='left', va='bottom', expand=0, label_params={}, **kwargs):
        img = np.array(img)

        ih, iw = img.shape[:2]

        x0, y0, w, h = rect

        force_aspect = False

        if w and h: force_aspect = True
        elif w: h = float(w) * ih / iw
        elif h: w = float(h) * iw / ih
        else: raise ValueError('must specify width or height for image')

        if va == 'top':
            y0 -= h
        elif va == 'center':
            y0 -= 0.5*h
        elif va != 'bottom':
            raise ValueError('va should be one of "bottom", "top", or "center"')

        if ha == 'right':
            x0 -= w
        elif ha == 'center':
            x0 -= 0.5*w
        elif ha != 'left':
            raise ValueError('ha should be one of "left", "right", or "center"')

        if expand:
            ex = float(expand) / iw
            ey = float(expand) / ih
            x0 -= w * ex
            w *= 1 + ex
            y0 -= h * ey
            h *= 1 + ex

        ax = self.add_axes((x0, y0, w, h), label=label, label_params=label_params)

        ax.imshow(img, clip_on=False, **kwargs)
        ax.set_xlim(-expand, iw+expand)
        ax.set_ylim(ih+expand, -expand)
        ax.set_axis_off()

        if force_aspect:
            ax.set_aspect('auto')

        return ax
