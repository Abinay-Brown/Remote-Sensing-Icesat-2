% data = readtable('TemporalModes_IcesatOnly.txt')
Imode1 = data{:,1};
Imode2 = data{:,2};
Imode3 = data{:,3};


t = linspace(1, 36, 36);

subplot(2, 1, 1);
plot(t, normalize(Imode1, 'scale'), 'LineWidth', 1);
title('Expansion Coefficient of Mode 1: 62.687%')
xlabel('time (months)');
ylabel('Normalized units')
axis([0 36 -6.5 1])
grid on;
subplot(2, 1, 2);
plot(t, normalize(Imode2, 'scale'), 'LineWidth', 1);
title('Expansion Coefficient of Mode 2: 27.754%')
xlabel('time (months)');
ylabel('Normalized units')
axis([0 36 -3.5 2.5])
grid on;
% subplot(3, 1, 3);
% plot(t, normalize(Imode3, 'scale'), 'LineWidth', 1);
% title('Expansion Coefficient of Mode 3: 0.92711%')
% xlabel('time (months)');
% ylabel('Normalized units')
% axis([0 36 -1 4.5])
% grid on;
% sgtitle('Icesat-2: Time Series of Expansion Coefficient')
