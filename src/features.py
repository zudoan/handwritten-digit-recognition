"""
Feature Engineering module for Handwritten Digit Recognition.
Implements:
1. Deskewing (Moments-based affine shear correction)
2. PCA (Principal Component Analysis dimensionality reduction)
3. HOG (Histogram of Oriented Gradients feature extraction)
4. Pipeline transformers for scikit-learn compatibility
"""
from typing import Tuple, Optional
import numpy as np
import cv2
from scipy.ndimage import interpolation
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from skimage.feature import hog


def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Deskew a single 28x28 grayscale image using central image moments.
    Computes covariance of the pixel intensity distribution and applies an
    affine shear transform to upright the digit.

    Mathematical principle:
        mu_11: covariance between x and y
        mu_02: variance along y
        skew = mu_11 / mu_02
        Affine transform: x' = x - skew * (y - cy)
    """
    # Calculate moments
    moments = cv2.moments(image)
    if abs(moments["mu02"]) < 1e-2:
        return image.copy()

    # Calculate skew
    skew = moments["mu11"] / moments["mu02"]

    # Transformation matrix
    M = np.float32([[1, skew, -0.5 * 28 * skew], [0, 1, 0]])

    # Apply warp affine
    deskewed = cv2.warpAffine(
        image,
        M,
        (28, 28),
        flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )
    return deskewed


def deskew_dataset(images: np.ndarray) -> np.ndarray:
    """
    Apply deskewing to an entire dataset of images.
    Images can be shape (N, 28, 28) or (N, 784).
    """
    orig_shape = images.shape
    if images.ndim == 2 and orig_shape[1] == 784:
        reshaped = images.reshape(-1, 28, 28)
    else:
        reshaped = images

    deskewed = np.empty_like(reshaped)
    for i in range(reshaped.shape[0]):
        deskewed[i] = deskew_image(reshaped[i])

    if images.ndim == 2:
        return deskewed.reshape(-1, 784)
    return deskewed


class DeskewTransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer for deskewing handwritten digit images.
    Takes 2D (N, 28, 28) or 1D (N, 784) images and returns deskewed 1D (N, 784) images.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return deskew_dataset(X)



def extract_hog_features(
    images: np.ndarray,
    orientations: int = 9,
    pixels_per_cell: Tuple[int, int] = (7, 7),
    cells_per_block: Tuple[int, int] = (2, 2),
) -> np.ndarray:
    """
    Extract Histogram of Oriented Gradients (HOG) features from image array.

    Args:
        images: Array of shape (N, 28, 28) or (N, 784).
        orientations: Number of gradient orientation bins (default 9).
        pixels_per_cell: Size of local cells in pixels (default (7, 7) -> 4x4 grid).
        cells_per_block: Number of cells in each block for normalization.

    Returns:
        Array of shape (N, num_hog_features).
    """
    if images.ndim == 2 and images.shape[1] == 784:
        images = images.reshape(-1, 28, 28)

    num_samples = images.shape[0]
    features_list = []
    for i in range(num_samples):
        feat = hog(
            images[i],
            orientations=orientations,
            pixels_per_cell=pixels_per_cell,
            cells_per_block=cells_per_block,
            block_norm="L2-Hys",
            transform_sqrt=True,
            feature_vector=True,
        )
        features_list.append(feat)

    return np.array(features_list, dtype=np.float32)


class DeskewTransformer(BaseEstimator, TransformerMixin):
    """Scikit-learn compatible transformer for deskewing digits."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return deskew_dataset(X)


class PCATransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-learn wrapper for PCA dimensionality reduction with variance threshold.
    """

    def __init__(self, n_components: float = 0.95, random_state: int = 42):
        self.n_components = n_components
        self.random_state = random_state
        self.pca = PCA(n_components=self.n_components, random_state=self.random_state)

    def fit(self, X, y=None):
        if X.ndim > 2:
            X = X.reshape(X.shape[0], -1)
        self.pca.fit(X)
        return self

    def transform(self, X):
        if X.ndim > 2:
            X = X.reshape(X.shape[0], -1)
        return self.pca.transform(X)

    @property
    def explained_variance_ratio_(self):
        return self.pca.explained_variance_ratio_

    @property
    def n_components_(self):
        return self.pca.n_components_


class HOGTransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-learn compatible transformer for extracting HOG features.
    """

    def __init__(
        self,
        orientations: int = 9,
        pixels_per_cell: Tuple[int, int] = (7, 7),
        cells_per_block: Tuple[int, int] = (2, 2),
    ):
        self.orientations = orientations
        self.pixels_per_cell = pixels_per_cell
        self.cells_per_block = cells_per_block

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return extract_hog_features(
            X,
            orientations=self.orientations,
            pixels_per_cell=self.pixels_per_cell,
            cells_per_block=self.cells_per_block,
        )

