a = 1;
alpha = 0;

Point(1) = {0, -1, 0, 1.0};
Point(2) = {0, 1, 0, 1.0};
Point(3) = {10, 1, 0, 1.0};
Point(4) = {10, -1, 0, 1.0};

Point(5) = {2 - a/2*Cos(alpha) + a/2*Sin(alpha), -a/2*Sin(alpha) - a/2*Cos(alpha), 0, 1.0};
Point(6) = {2 + a/2*Cos(alpha) + a/2*Sin(alpha), a/2*Sin(alpha) - a/2*Cos(alpha), 0, 1.0};
Point(7) = {2 + a/2*Cos(alpha) - a/2*Sin(alpha), a/2*Sin(alpha) + a/2*Cos(alpha), 0, 1.0};
Point(8) = {2 - a/2*Cos(alpha) - a/2*Sin(alpha), -a/2*Sin(alpha) + a/2*Cos(alpha), 0, 1.0};

Point(9) = {2 - a/2*Cos(alpha) - a/2*Sin(alpha), 1, 0, 1.0};
Point(10) = {2 - a/2*Cos(alpha) + a/2*Sin(alpha), -1, 0, 1.0};
Point(11) = {2 + a/2*Cos(alpha) + a/2*Sin(alpha), -1, 0, 1.0};
Point(12) = {2 + a/2*Cos(alpha) - a/2*Sin(alpha), 1, 0, 1.0};
Point(13) = {0, -a/2*Sin(alpha) + a/2*Cos(alpha), 0, 1.0};
Point(14) = {0, -a/2*Sin(alpha) - a/2*Cos(alpha), 0, 1.0};
Point(15) = {10, a/2*Sin(alpha) - a/2*Cos(alpha), 0, 1.0};
Point(16) = {10, a/2*Sin(alpha) + a/2*Cos(alpha), 0, 1.0};

Line(1) = {9, 2};
Line(2) = {2, 13};
Line(3) = {13, 8};
Line(4) = {8, 9};
Line(5) = {9, 12};
Line(6) = {12, 7};
Line(7) = {7, 8};
Line(8) = {13, 14};
Line(9) = {14, 5};
Line(10) = {5, 8};
Line(11) = {7, 6};
Line(12) = {6, 5};
Line(13) = {10, 5};
Line(14) = {14, 1};
Line(15) = {1, 10};
Line(16) = {10, 11};
Line(17) = {11, 4};
Line(18) = {4, 15};
Line(19) = {15, 15};
Line(20) = {16, 16};
Line(21) = {15, 16};
Line(22) = {16, 3};
Line(23) = {3, 12};
Line(24) = {6, 11};
Line(25) = {6, 15};
Line(26) = {16, 7};

Line Loop(27) = {1, 2, 3, 4};
Plane Surface(28) = {27};
Line Loop(29) = {5, 6, 7, 4};
Plane Surface(30) = {29};
Line Loop(31) = {3, -10, -9, -8};
Plane Surface(32) = {31};
Line Loop(33) = {14, 15, 13, -9};
Plane Surface(34) = {33};
Line Loop(35) = {12, -13, 16, -24};
Plane Surface(36) = {35};
Line Loop(37) = {25, -18, -17, -24};
Plane Surface(38) = {37};
Line Loop(39) = {21, 26, 11, 25};
Plane Surface(40) = {39};
Line Loop(41) = {6, -26, 22, 23};
Plane Surface(42) = {41};

Transfinite Line {8, 10, 11, 21, 5, 7, 12, 16} = 10 Using Progression 1;
Transfinite Line {2, 4, 6, 22, 18, 24, 13, 14} = 5 Using Progression 1;
Transfinite Line {1, 3, 9, 15} = 15 Using Progression 1;
Transfinite Line {23, 26, 25, 17} = 25 Using Progression 1;

Transfinite Surface {28};
Transfinite Surface {32};
Transfinite Surface {34};
Transfinite Surface {36};
Transfinite Surface {30};
Transfinite Surface {42};
Transfinite Surface {40};
Transfinite Surface {38};
Recombine Surface {28, 32, 34, 36, 30, 42, 40, 38};

Physical Line("inlet") = {2, 8, 14};
Physical Line("outlet") = {22, 21, 18};
Physical Line("wall") = {1, 5, 23, 15, 16, 17};
Physical Line("square") = {7, 10, 12, 11};
Physical Surface("volume") = {28, 32, 34, 36, 30, 42, 40, 38};

