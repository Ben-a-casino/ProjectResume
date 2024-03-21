using Plots, Roots, LaTeXStrings

x_dot(x, r) = r - x - exp(-1*x)

xs = range(-2.2, 2.2, length = 50)

p1 = plot(framestyle=:origin, legend = false)

for rs in [-1 0 1 2]#range(-1, 1, length = 50)#collect(-10:2:10)
    plot!(p1, xs, x_dot.(xs, rs))#, label = "["*string(as)*", "*string(bs)*"]")
end    
xlabel!(p1, L"x")
ylabel!(p1, L"\dot{x}")
    
@show p1

x_dot(x, r) = r - x - exp(-1*x)
fx_dot(x) = -1 + exp(-1*x)

p1 = plot(framestyle=:origin, legend = false)

for R in range(-5, 5, length = 100)
    roots = Roots.find_zeros(x -> R - x - exp(-1*x), xs[1], xs[end])
    for r in roots
        lin_test = fx_dot(r)
        if lin_test < 0
            scatter!(p1, [R], [r], color = "#FF0000")
        elseif lin_test > 0
            scatter!(p1, [R], [r], color = "#FFFFFF")
        else
            scatter!(p1, [R], [r], color = "#FFC0CB")
        end
    end
end

@show p1

x_dot(x, a, b) = x*(1-x^2) - a*(1-exp(-1*b*x))

xs = range(-2.2, 2.2, length = 50)

p1 = plot(framestyle=:origin, legend = false)

for as in [-1]#collect(-10:2:10)
    for bs in [-1 0 1]#range(-1, 1, length = 50)#collect(-10:2:10)
        plot!(p1, xs, x_dot.(xs, as, bs))#, label = "["*string(as)*", "*string(bs)*"]")
    end    
end
xlabel!(p1, L"x")
ylabel!(p1, L"\dot{x}")
    
@show p1

a = 1
x_dot(x) = x*(1-x^2) - a*(1-exp(-1*b*x))
fx_dot(x, a, b) = 1 - 3*x^2 - a*b*exp(-1*b*x)

p1 = plot(framestyle=:origin, legend = false)


for b in range(-1.5, 1.5, length = 100)
    roots = Roots.find_zeros(x -> x*(1-x^2) - a*(1-exp(-1*b*x)), xs[1], xs[end])
    for r in roots
        lin_test = fx_dot(r, a, b)
        if lin_test < 0
            scatter!(p1, [b], [r], color = "#FF0000")
        elseif lin_test > 0
            scatter!(p1, [b], [r], color = "#FFFFFF")
        else
            scatter!(p1, [b], [r], color = "#FFC0CB")
        end
    end
end

@show p1

x_dot(x) = x*(1-x^2) - a*(1-exp(-1*b*x))
fx_dot(x, a, b) = 1 - 3*x^2 - a*b*exp(-1*b*x)

A = range(-1, 1, length = 50)
B = range(-1, 1, length = 50)

bifur_mat = []

for a in A
    for b in B
        roots = find_zeros(x -> x*(1-x^2) - a*(1-exp(-1*b*x)), xs[1], xs[end])
        for r in roots
            lin_test = fx_dot(r, a, b)
            if lin_test < 0
                bifur_mat = vcat(bifur_mat, [a b r -1])
            elseif lin_test > 0
                bifur_mat = vcat(bifur_mat, [a b r 1])
            else
                bifur_mat = vcat(bifur_mat, [a b r 0])
            end
        end
    end
end

# bifur_mat

p1 = scatter(bifur_mat[:,1], bifur_mat[:,2], bifur_mat[:,3], zcolor = bifur_mat[:,4], legend = false, color=:PRGn_3)#, camera=(-45,-45))

# @show p1

x_dot(x) = x*(1-x^2) - a*(1-exp(-1*b*x))
fx_dot(x, a, b) = 1 - 3*x^2 - a*b*exp(-1*b*x)

p1 = plot(legend = false)#, camera=(-45,-45))
for a in range(-1, 1, length = 50)
    for b in range(-1, 1, length = 50)
        roots = find_zeros(x -> x*(1-x^2) - a*(1-exp(-1*b*x)), xs[1], xs[end])
        for r in roots
            lin_test = fx_dot(r, a, b)
            if lin_test < 0
                scatter!(p1, [a], [b], [r], color = "#FF0000")
            elseif lin_test > 0
                scatter!(p1, [a], [b], [r], color = "#FFFFFF")
            else
                scatter!(p1, [a], [b], [r], color = "#FFC0CB")
            end
        end
    end
end
@show p1






