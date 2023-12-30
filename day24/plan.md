# Problem 24b

## Observation

* Let $\vec{v}$ be the direction we wil throw the rock.
* Let $t_n$ be the number of ns it takes for each hail to impact the rock.

If we project all lines to the plane defined with $\vec{v}$ as the normal, they should all intersect at a single point.

## Plan
1. Algorithm to find $\vec{v}$.
    1. Initialize $\vec{v}$ to a random direction.
    3. Determine where vectors intersect plane with $\vec{v}$ as normal.
        1. For each $\vec{x_i}$: 2 points: $\vec{x}_{i0}$ and $\vec{x}_{i1}$.
            * $\vec{x}_{i0} \coloneqq \text{Starting position}$
            * $\vec{x}_{i1} \coloneqq \vec{x}_{i0}$ + $10^{12} * \vec{v}_{i0}$
        2. Get 4 vectors $\vec{x_i}$ from input.
        2. Project onto plane:
            * $\vec{x}_{i0}^\prime \coloneqq \vec{x}_{i0} - \vec{x}_{i0} \cdot{} \vec{v}$
            * $\vec{x}_{i1}^\prime \coloneqq \vec{x}_{i1} - \vec{x}_{i1} \cdot{} \vec{v}$
        2. Project onto x-y plane:
            * $\vec{x}_{i0}^{\prime\prime} \coloneqq \vec{x}_{i0} - \vec{x}_{i0}^\prime \cdot{} (0,0,1)$
            * $\vec{x}_{i1}^{\prime\prime} \coloneqq \vec{x}_{i1} - \vec{x}_{i1}^\prime \cdot{} (0,0,1)$
        2. Find line intersections between all 4.
            * $\vec{y}_{i0}^{\prime\prime} \coloneqq \text{v2intersect(}\vec{x}_{i0}^{\prime\prime}, \vec{x}_{i1}^{\prime\prime},\vec{x}_{\text{(}i+1\text{)}0}^{\prime\prime},\vec{x}_{{\text{(}i+1\text{)}}1}^{\prime\prime}\text{)}$
            * $\vec{y}_{i1}^{\prime\prime} \coloneqq \vec{x}_{i1}^\prime \cdot{} (0,0,1)$
        3. Let $d$ be the max distance between intersection points.
        3. Iteratively reduce d by adjusting $\vec{v}$







2. Determine intersection points, which allows us to determine $t_n$.
i


$$
L(p') :=qp \\
r =(cos^2(\theta/2) - norm(u)^2) p + 2(u\cdot{}p)u + 2cos(\theta/2)(u*p) \\
n_t = n * u
$$

$$
L(0,n) = (0,(cos^2(\theta/2) - sin^2(\theta/2))n+ 2(cos^2(\theta/2)sin^2(\theta/2))n_T \\
= cos(\theta)n + sin(\theta)n_T
$$

$$
L(0,n) = (0,(cos^2(\theta/2) - sin^2(\theta/2))n+ 2(cos(\theta/2)sin(\theta/2))n_T \\
= cos(\theta)n + sin(\theta)n_T
$$

$$
1 = sin^2(\theta) + cos^2(\theta) \\
1 - sin^2(\theta) = cos^2(\theta)
$$

Quaternion rotation:
$$
q = cos(\theta/2) + u * sin(\theta/2) \\
q^{-1} = cos(\theta/2) - u * sin(\theta/2) \\
L(p) = qpq^{-1}
$$

"unrotate" $v$, unit vector in $\mathbb{R}^3$:
$$
\vec{n} := \vec{v}/{||\vec{v}||} \\
\phi = sin^{-1}(n_z) \\
\theta = cos^{-1}(n_x^2/(n_x^2+n_y^2))

$$
