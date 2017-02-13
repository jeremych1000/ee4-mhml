%function to calculate the instant SVM sample by sample

function output = calinstant(x ,y ,z)
  temp = x*x + y*y + z*z;
  output = sqrt(temp);
end