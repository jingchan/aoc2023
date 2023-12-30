
# ### Derive line intersection formula from line equations.
#

let $(x,y)$ be point where the following two intersect:

- stone1: (position: $\vec{x}_1$, velocity: $\Delta\vec{x}_1$)
- stone2: (position: $\vec{x}_2$, velocity: $\Delta\vec{x}_2$)

They intersect when:

$$
\vec{x} = \vec{x}_{1} + \Delta\vec{x}_{1}*t_1 = \vec{x}_{2} + \Delta\vec{x}_{2}*t_2 \\
$$

Since the x and y dimensions are independent of each other, we can expand this into 2 equations:

Solve for $t_1$:
$$
x_1 + \Delta x_1*t_1 = x_2 + \Delta x_2*t_2 \\
$$
Subtract $x_1$ from both sides:
$$
\Delta x_1*t_1 = x_2 + \Delta x_2*t_2 - x_1
$$
$$
t_1 = (x_2 + \Delta x_2*t_2 - x_1)/ \Delta x_1\\
$$

<!-- $$
y_1 + \Delta y_1*t_1 = y_2 + \Delta y_2*t_2 \\
$$ -->


<!--
#     (x0 + v_x0*t0 - x1) / v_x1 = t1
# y = y0 + v_y0*t0 = y1 + v_y1*t1
#     (y0 + v_y0*t0 - y1) / v_y1 = t1
#
#     x0*v_y1 + v_x0*v_y1*t0 - x1*v_y1 = y0*v_x1 + v_y0*v_x1*t0 - y1*v_x1
#     v_x0*v_y1*t0 - v_y0*v_x1*t0 = y0*v_x1 - y1*v_x1 - x0*v_y1 + x1*v_y1
#     t0*(v_x0*v_y1 - v_y0*v_x1) = y0*v_x1 - y1*v_x1 - x0*v_y1 + x1*v_y1
#     t0 = (y0*v_x1 - y1*v_x1 - x0*v_y1 + x1*v_y1) / (v_x0*v_y1 - v_y0*v_x1)
#     t1 = (x0 + v_x0*t0 - x1) / v_x1 -->
