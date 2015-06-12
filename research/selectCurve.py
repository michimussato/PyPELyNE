from math import sqrt
from sys import argv

from PyQt4.Qt import QApplication
from PyQt4.QtCore import QPoint, QPointF, Qt
from PyQt4.QtGui import (
    QColor,
    QGraphicsItem,
    QGraphicsView,
    QGraphicsScene,
    QPainterPath,
)


class View(QGraphicsView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.epsilon = 11.0
        self.graphics_scene = QGraphicsScene(self)
        self.setScene(self.graphics_scene)
        self.add_curve()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.select_item_at(event.x(), event.y())

    def select_item_at(self, x, y):
        point = self.mapToScene(QPoint(x, y))
        self.unselect_items()
        for item in self.items():
            if item.contains_point(point.x(), point.y(), self.epsilon):
                item.set_selected(True)
                item.update()

    def unselect_items(self):
        for item in self.items():
            item.set_selected(False)
            item.update()

    def add_curve(self):
        color = QColor(255, 0, 0)
        x0 = 600.0
        y0 = 400.0
        x1 = 800.0
        y1 = 500.0
        x2 = 1000.0
        y2 = 500.0
        x3 = 1200.0
        y3 = 400.0
        control_points = (QPointF(x0, y0), QPointF(x1, y1),
            QPointF(x2, y2), QPointF(x3, y3))
        curve = Curve(color, control_points)
        self.graphics_scene.addItem(curve)


class Curve(QGraphicsItem):
    def __init__(self, color, control_points, parent=None, scene=None):
        super(Curve, self).__init__(parent, scene)
        self.selected = False
        self.color = color
        self.path = QPainterPath()
        self.path.moveTo(control_points[0])
        self.path.cubicTo(*control_points[1:])

    def set_selected(self, selected):
        self.selected = selected

    def contains_point(self, x, y, epsilon):
        p = (x, y)
        min_distance = float(0x7fffffff)
        t = 0.0
        while t < 1.0:
            point = self.path.pointAtPercent(t)
            spline_point = (point.x(), point.y())
            print p, spline_point
            distance = self.distance(p, spline_point)
            if distance < min_distance:
                min_distance = distance
            t += 0.1
        print min_distance, epsilon
        return (min_distance <= epsilon)

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter, option, widget):
        painter.setPen(self.color)
        painter.setBrush(self.color)
        painter.strokePath(self.path, painter.pen())

    def distance(self, p0, p1):
        a = p1[0] - p0[0]
        b = p1[1] - p0[1]
        return sqrt(a * a + b * b)


if __name__ == '__main__':
    app = QApplication(argv)
    view = View()
    view.setGeometry(100, 100, 1600, 900)
    view.setWindowTitle('MainWindow')
    view.show()
    app.exec_()