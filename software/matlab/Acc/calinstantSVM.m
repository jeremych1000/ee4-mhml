%function to calculate instantSVM
%input x y z in vector

function instantSVM = calinstantSVM(x, y, z)
x_square = x.*x;
y_square = y.*y;
z_square = z.*z;
sum_of_squared = x_square + y_square + z_square;
instantSVM = sqrt(sum_of_squared);

end