data = readtable('TemporalModes_IG.txt')
Imode1 = data{:,1};
Imode2 = data{:,2};
Imode3 = data{:,3};

Gmode1 = data{:,4};
Gmode2 = data{:,5};
Gmode3 = data{:,6};

t = linspace(1, 36, 36);

% subplot(3, 1, 1);
% plot(t, normalize(Imode1, 'scale'), 'LineWidth', 1);
% title('Expansion Coefficient of Mode 1: 99.956%')
% xlabel('time (months)');
% ylabel('Normalized units')
% axis([0 36 -6 2])
% grid on;
% subplot(3, 1, 2);
% plot(t, normalize(Imode2, 'scale'), 'LineWidth', 1);
% title('Expansion Coefficient of Mode 2: 0.03661%')
% xlabel('time (months)');
% ylabel('Normalized units')
% axis([0 36 -6 2.4])
% grid on;
% subplot(3, 1, 3);
% plot(t, normalize(Imode3, 'scale'), 'LineWidth', 1);
% title('Expansion Coefficient of Mode 3: 0.001954%')
% xlabel('time (months)');
% ylabel('Normalized units')
% axis([0 36 -4 4.5])
% grid on;
% sgtitle('Icesat-2: Time Series of Expansion Coefficient')

subplot(3, 1, 1);
plot(t, normalize(Gmode1, 'scale'), 'LineWidth', 1);
title('Expansion Coefficient Mode 1: 99.956%')
xlabel('time (months)');
ylabel('Normalized units')
axis([0 36 -1.7 1])
grid on;
subplot(3, 1, 2);
plot(t, normalize(Gmode2, 'scale'), 'LineWidth', 1);
title('Expansion Coefficient Mode 2: 0.03661%')
xlabel('time (months)');
ylabel('Normalized units')
axis([0 36 -1 2.5])
grid on;
subplot(3, 1, 3);
plot(t, normalize(Gmode3, 'scale'), 'LineWidth', 1);
title('Expansion Coefficient Mode 3: 0.001954%')
xlabel('time (months)');
ylabel('Normalized units')
axis([0 36 -4 2])
grid on;
sgtitle('GRACE: Time Series of Expansion Coefficient')