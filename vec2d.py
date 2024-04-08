import math

class Point:
    
    """
    Represents a point in 2-dimensional space.
    Attributes
    -------    
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    """
    Initialize a new Point instance.

    Parameters
    -------
        x (float): The x-coordinate of the point. Default is 0.
        y (float): The y-coordinate of the point. Default is 0.
    Returns
    -------
    None
    """

    def __str__(self):
        return f"x: {self.x} y: {self.y}"
    """
    Return a string representation of the point.

    Returns
    -------
        str: A string that represents the point's coordinates.

    """

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return NotImplemented
    """
    Add two points' coordinates.
    Parameters
    -------
        other (Point): Another point to add to this one.
    Returns
    -------
        Point: A new point that is the sum of this one and the other.
    """

    def __iadd__(self, other):
        if isinstance(other, Point):
            self.x += other.x
            self.y += other.y
            return self
        return NotImplemented
        """
    Performs in-place addition of this point's coordinates with another.

    Parameters
    -------
        other (Point): Another point to add to this one.

    Returns
    -------
        Point: This instance after adding the other point's coordinates.
    """

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return NotImplemented
    """
    Subtract another point's coordinates from this one's.
    Parameters
    -------
        other (Point): Another point to subtract from this one.
    Returns
    -------
        Point: A new point that is the difference between this one and the other.
    """
    def __isub__(self, other):
        if isinstance(other, Point):
            self.x -= other.x
            self.y -= other.y
            return self
        return NotImplemented
    """
    Performs in-place subtraction of another point's coordinates from this one's.

    Parameters
    -------
        other (Point): Another point to subtract from this one.

    Returns
    -------
        Point: This instance after subtracting the other point's coordinates.
    """


class Vec2D(Point):
    """
    Represents a 2-dimensional vector, extending a Point with vector-specific operations.

    Inherits from the Point class, adding methods for vector magnitude, normalization,
    and arithmetic operations specific to vectors.
    """
    def __init__(self, *args):
        # Handle initialization with a single Point, setting vector based on point position
        if len(args) == 1 and isinstance(args[0], Point):
            super().__init__(args[0].x, args[0].y)
        # Handle initialization with two Points, creating a vector from the first to the second
        elif len(args) == 2 and all(isinstance(arg, Point) for arg in args):
            super().__init__(args[1].x - args[0].x, args[1].y - args[0].y)
        # Handle initialization with x and y components
        elif len(args) == 2 and all(isinstance(arg, (int, float)) for arg in args):
            super().__init__(*args)
        # Default initialization or incorrect input types
        else:
            super().__init__(0, 0) 
    """
    Initialize a new Vec2D instance. Can be initialized with two points (defining a vector),
    a single point (origin to point vector), or x and y components directly.

    Parameters
    -------
        *args: Variable length argument list allowing for multiple types of initialization.
    Returns
    -------
    None
    """
    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    """
    Compute the norm (magnitude) of the vector.

    Returns
    -------
        float: The Euclidean norm of the vector.
    """
    def __add__(self, other):
        result = super().__add__(other)
        if result is not NotImplemented:
            return Vec2D(result.x, result.y)
        return NotImplemented
    """
    Add a Vec2D or Point to this vector, returning a new Vec2D instance.
        
    overrides the Point class's __add__ method to ensure the result is a Vec2D instance.

    Parameters
    -------
         other (Vec2D | Point): The vector or point to add.

    Returns
    -------
        Vec2D: A new vector that is the sum of this vector and the other.
    """
    def __sub__(self, other):
        result = super().__sub__(other)
        if result is not NotImplemented:
            return Vec2D(result.x, result.y)
        return NotImplemented
    """
    Subtract a Vec2D or Point from this vector, returning a new Vec2D instance.
        
    Overrides the Point class's __sub__ method to ensure the result is a Vec2D instance.

    Parameters
    -------
        other (Vec2D | Point): The vector or point to subtract.

    Returns
    -------
        Vec2D: A new vector that is the difference between this vector and the other.
    """


    def __mul__(self, other):
        if isinstance(other, (Vec2D, Point)):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vec2D(self.x * other, self.y * other)
        return NotImplemented
    """
    This multiplies this vector by another vector or a scalar. If other is a vector, the method 
    returns the dot product.If the other is a scalar, it returns a new Vec2D scaled by a scalar.
    Parameters
    -------
         other (Vec2D | Point | int | float): The vector or scalar to multiply with.
    Returns
    -------
         float | Vec2D: The dot product (if other is a vector) or a new, scaled Vec2D (if other is a scalar).
    """

    def normal_ccw(self):
        return Vec2D(-self.y, self.x)
    """
    Compute a counterclockwise normal vector to this vector.
    Returns
    -------
        Vec2D: A new vector that is perpendicular to this one, rotated counterclockwise.
    """
