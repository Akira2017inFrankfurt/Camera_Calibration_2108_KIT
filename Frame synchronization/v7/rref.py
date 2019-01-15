#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def rref(B, tol=1e-15, debug=False):
	A = B.copy()
	rows, cols = A.shape
	r = 0
	pivots_pos = []
	row_exchanges = np.arange(rows)
	for c in xrange(cols):
		if debug:
			print "Now at row", r, "and col", c, "with matrix:"; print A

		## Find the pivot row:
		pivot = np.argmax (np.abs (A[r:rows,c])) + r
		m = np.abs(A[pivot, c])
		if debug:
			print "Found pivot", m, "in row", pivot
		if m <= tol:
			## Skip column c, making sure the approximately zero terms are
			## actually zero.
			A[r:rows, c] = np.zeros(rows-r)
			if debug:
				print "All elements at and below (", r, ",", c, ") are zero.. moving on.."
		else:
			## keep track of bound variables
			pivots_pos.append((r,c))

			if pivot != r:
				## Swap current row and pivot row
				A[[pivot, r], c:cols] = A[[r, pivot], c:cols]
				row_exchanges[[pivot,r]] = row_exchanges[[r,pivot]]

				if debug:
					print "Swap row", r, "with row", pivot, "Now:"; print A

			## Normalize pivot row
			A[r, c:cols] = A[r, c:cols] / A[r, c];

			## Eliminate the current column
			v = A[r, c:cols]
			## Above (before row r):
			if r > 0:
				ridx_above = np.arange(r)
				A[ridx_above, c:cols] = A[ridx_above, c:cols] - np.outer(v, A[ridx_above, c]).T
				if debug:
					print "Elimination above performed:"; print A
			## Below (after row r):
			if r < rows-1:
				ridx_below = np.arange(r+1,rows)
				A[ridx_below, c:cols] = A[ridx_below, c:cols] - np.outer(v, A[ridx_below, c]).T
				if debug:
					print "Elimination below performed:"; print A
			r += 1
		## Check if done
		if r == rows:
			break;
	return A



