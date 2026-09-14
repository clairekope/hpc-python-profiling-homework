"""Solve a 2D Poisson problem using a dense linear system."""

from __future__ import annotations

import numpy as np


def validate_grid(nx: int, ny: int) -> None:
    """Check that the grid has an interior region large enough to solve."""
    if nx < 3 or ny < 3:
        raise ValueError("nx and ny must be at least 3 so there is at least one interior point.")


def build_grid(nx: int, ny: int) -> tuple[np.ndarray, np.ndarray]:
    """Create the physical coordinates for the domain."""
    x = np.linspace(0.0, 1.0, nx)
    y = np.linspace(0.0, 1.0, ny)
    return x, y


def interior_index(interior_nx: int, i: int, j: int) -> int:
    """Map a 2D interior grid location to a 1D dense-matrix index."""
    return (j - 1) * interior_nx + (i - 1)


def assemble_poisson_system(nx: int, ny: int, source_value: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Assemble the dense matrix and right-hand side for the Poisson problem."""
    x, y = build_grid(nx, ny)
    interior_nx = nx - 2
    interior_ny = ny - 2
    n_unknowns = interior_nx * interior_ny

    hx = x[1] - x[0]
    hy = y[1] - y[0]

    A = np.zeros((n_unknowns, n_unknowns), dtype=float)
    b = np.zeros(n_unknowns, dtype=float)

    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            n = interior_index(interior_nx, i, j)
            b[n] = source_value

            A[n, n] = 2.0 / hx**2 + 2.0 / hy**2

            if i > 1:
                A[n, interior_index(interior_nx, i - 1, j)] = -1.0 / hx**2
            if i < nx - 2:
                A[n, interior_index(interior_nx, i + 1, j)] = -1.0 / hx**2
            if j > 1:
                A[n, interior_index(interior_nx, i, j - 1)] = -1.0 / hy**2
            if j < ny - 2:
                A[n, interior_index(interior_nx, i, j + 1)] = -1.0 / hy**2

    return A, b, x, y


def solve_dense_system(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Solve the dense linear system by manual Gaussian elimination."""
    n = len(b)
    M = A.copy()
    x = b.copy()

    for k in range(n):
        pivot_row = max(range(k, n), key=lambda r: abs(M[r, k]))
        if abs(M[pivot_row, k]) < 1e-14:
            raise ValueError("Matrix is singular or ill-conditioned.")

        if pivot_row != k:
            M[[k, pivot_row], :] = M[[pivot_row, k], :]
            x[[k, pivot_row]] = x[[pivot_row, k]]

        pivot = M[k, k]
        for j in range(k, n):
            M[k, j] /= pivot
        x[k] /= pivot

        for i in range(k + 1, n):
            factor = M[i, k]
            if factor == 0.0:
                continue
            for j in range(k, n):
                M[i, j] -= factor * M[k, j]
            x[i] -= factor * x[k]

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            x[i] -= M[i, j] * x[j]

    return x


def expand_solution(u_interior: np.ndarray, nx: int, ny: int) -> np.ndarray:
    """Place interior values back into the full grid, with zero boundaries."""
    u = np.zeros((ny, nx), dtype=float)
    interior_nx = nx - 2

    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            u[j, i] = u_interior[interior_index(interior_nx, i, j)]

    return u


def compute_residual(A: np.ndarray, u_interior: np.ndarray, b: np.ndarray) -> float:
    """Compute the maximum absolute residual of the linear solve."""
    return float(np.max(np.abs(A @ u_interior - b)))


def solve_poisson_problem(nx: int = 101, ny: int = 101, source_value: float = 1.0):
    """Solve -Δu = f on a 2D grid with zero Dirichlet boundary conditions.

    This dense version is intentionally slow for profiling demonstrations.

    Returns
    -------
    u : ndarray, shape (ny, nx)
        The solution values on the full grid.
    x : ndarray, shape (nx,)
        x coordinates.
    y : ndarray, shape (ny,)
        y coordinates.
    residual : float
        Maximum absolute residual from the dense solve.
    """
    validate_grid(nx, ny)
    A, b, x, y = assemble_poisson_system(nx, ny, source_value)
    u_interior = solve_dense_system(A, b)
    u = expand_solution(u_interior, nx, ny)
    residual = compute_residual(A, u_interior, b)
    return u, x, y, residual
