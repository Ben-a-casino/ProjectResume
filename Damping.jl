using Plots, LaTeXStrings, VectorFieldPlots

# Harmonic Oscillator with damping
# Code from: https://github.com/maxhcohen/VectorFieldPlots.jl
# Plot defaults so things look nice
default(grid=false, framestyle=:box, label="", fontfamily="Computer Modern")

# Parameters 
k = 1
m = 4
c = 2
ω = sqrt(k/m)
ζ = c/(2*m*ω)

# Define vector field
f(x1, x2) = [x2, (-2*ζ*ω*x2) - (ω^2*x1)]

# Region to plot vector field over
x1s = -5.0:0.5:5.0
x2s = -5.0:0.5:5.0

# Coordinates for initial conditions of phase portraits and length of corresponding sim
x1s_phase = -3.0:3.0
x2s_phase = -3.0:3.0
T = 100.0

# Plot the vector field
fig = plot_vector_field(x1s, x2s, f, scale=0.35)
plot_phase_portrait!(x1s_phase, x2s_phase, f, T)
xlabel!(L"x_1")
ylabel!(L"x_2")
xlims!(-5, 5)
display(fig)


delta_t = 0.01
times = collect(0:delta_t:20)
times_size = length(times)

x1 = zeros(times_size)
x2 = zeros(times_size)
x1[1] = 1 #intial condition
x2[1] = 1 #intial condition
for n in 1:(times_size-1)
    x1[n+1], x2[n+1] = [x1[n], x2[n]] .+ (delta_t .* f(x1[n], x2[n]) )
end

plot(times, x1)





