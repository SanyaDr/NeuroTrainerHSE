import { useState, useEffect } from "react";
import "./App.css";

import angryImg from "./assets/angry.png";
import happyImg from "./assets/happy.png";
import sleepyImg from "./assets/sleepy2.png";
import profileIcon from "./assets/account-circle-outline.png";
import catImg from "./assets/cat.png";

const TABS = {
  TRAINING: "training",
  HISTORY: "history",
  STATS: "stats",
};

const moodToImage = {
  злое: angryImg,
  сонное: sleepyImg,
  бодрое: happyImg,
};

/* ===== ХЕЛПЕРЫ ВРЕМЕНИ ===== */

function formatSeconds(sec) {
  const m = Math.floor(sec / 60)
    .toString()
    .padStart(2, "0");
  const s = Math.floor(sec % 60)
    .toString()
    .padStart(2, "0");
  return `${m}:${s}`;
}

function parseDurationToSeconds(str) {
  const parts = str.split(":");
  if (parts.length !== 2) return 30 * 60;
  const m = parseInt(parts[0], 10);
  const s = parseInt(parts[1], 10);
  if (Number.isNaN(m) || Number.isNaN(s)) return 30 * 60;
  return m * 60 + s;
}

/* ===== ДЕМО-ДАННЫЕ ДЛЯ ИСТОРИИ ===== */

const baseExercises = [
  {
    sets: 2,
    name: "обратные отжимания от стула",
    status: "выполнено",
    points: 3,
  },
  {
    sets: 4,
    name: "обратные отжимания от стула",
    status: "выполнено",
    points: 3,
  },
  {
    sets: 0,
    name: "обратные отжимания от стула",
    status: "скип",
    points: 3,
  },
];

const historyData = [
  {
    id: 1,
    datetime: "12.01.2025 21:30",
    mood: "бодрое",
    mode: "турбо",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 2,
    datetime: "11.01.2025 07:15",
    mood: "сонное",
    mode: "тихий апгрейд",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 3,
    datetime: "10.01.2025 18:40",
    mood: "злое",
    mode: "турбо",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 4,
    datetime: "09.01.2025 23:05",
    mood: "сонное",
    mode: "турбо",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 5,
    datetime: "08.01.2025 16:20",
    mood: "бодрое",
    mode: "тихий апгрейд",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 6,
    datetime: "07.01.2025 10:55",
    mood: "злое",
    mode: "турбо",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 7,
    datetime: "06.01.2025 14:10",
    mood: "сонное",
    mode: "турбо",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 8,
    datetime: "05.01.2025 20:45",
    mood: "бодрое",
    mode: "турбо",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 9,
    datetime: "04.01.2025 06:30",
    mood: "злое",
    mode: "тихий апгрейд",
    totalPoints: 9,
    exercises: baseExercises,
  },
  {
    id: 10,
    datetime: "03.01.2025 19:00",
    mood: "сонное",
    mode: "турбо",
    totalPoints: 9,
    exercises: baseExercises,
  },
];

/* ===== РАДАР-ДИАГРАММА (ГИБКОСТЬ / СИЛА / ВЫНОСЛИВОСТЬ) ===== */

function StatsRadar({ flexibility, strength, endurance }) {
  const size = 220;
  const center = size / 2;
  const maxRadius = size / 2 - 20;
  const maxValue = 100;

  const data = [
    { label: "гибкость", value: flexibility },
    { label: "сила", value: strength },
    { label: "выносливость", value: endurance },
  ];

  const angleStep = (Math.PI * 2) / data.length;

  const pointByFactor = (factor, index) => {
    const angle = -Math.PI / 2 + angleStep * index; // старт сверху
    const r = maxRadius * factor;
    const x = center + r * Math.cos(angle);
    const y = center + r * Math.sin(angle);
    return [x, y];
  };

  // уровни сетки
  const gridLevels = [1 / 3, 2 / 3, 1];

  const gridPolygons = gridLevels.map((level, lvlIndex) => {
    const pts = data
      .map((_, i) => pointByFactor(level, i))
      .map((p) => p.join(","))
      .join(" ");
    return (
      <polygon
        key={lvlIndex}
        points={pts}
        fill="none"
        stroke="#6b7280"
        strokeWidth="0.5"
      />
    );
  });

  const axes = data.map((item, index) => {
    const [x, y] = pointByFactor(1, index);
    return (
      <line
        key={item.label}
        x1={center}
        y1={center}
        x2={x}
        y2={y}
        stroke="#6b7280"
        strokeWidth="0.5"
      />
    );
  });

  const valuePoints = data
    .map((item, index) => {
      const factor = Math.max(0, Math.min(1, item.value / maxValue));
      return pointByFactor(factor, index);
    })
    .map((p) => p.join(","))
    .join(" ");

  const labels = data.map((item, index) => {
    const labelRadiusFactor = 1.02;
    const [x, y] = pointByFactor(labelRadiusFactor, index);
    return (
      <text
        key={item.label}
        x={x}
        y={y}
        textAnchor="middle"
        dominantBaseline="middle"
        className="stats-radar-label"
      >
        {item.label}
      </text>
    );
  });

  return (
    <svg
      className="stats-radar"
      viewBox={`0 0 ${size} ${size}`}
      role="img"
      aria-label="Радар статистики"
    >
      <g>
        {gridPolygons}
        {axes}
        <polygon
          points={valuePoints}
          fill="rgba(59,130,246,0.35)"
          stroke="#3b82f6"
          strokeWidth="1"
        />
        {labels}
      </g>
    </svg>
  );
}

/* ===== ГРАФИК НАСТРОЕНИЯ ПО ДНЯМ НЕДЕЛИ ===== */

const moodLevels = ["злое", "сонное", "бодрое"];
const dayNames = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"];

// демо-данные: настроение по дням недели
const weekMoods = [
  "сонное",   // пн
  "злое",     // вт
  "бодрое",   // ср
  "бодрое",   // чт
  "сонное",   // пт
  "злое",     // сб
  "бодрое",   // вс
];

function MoodChart({ moods }) {
  const width = 720;
  const height = 260;
  const margin = { top: 20, right: 20, bottom: 35, left: 70 };

  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const maxMoodIndex = moodLevels.length - 1;
  const stepX =
    moods.length > 1 ? innerWidth / (moods.length - 1) : innerWidth;
  const stepY = innerHeight / maxMoodIndex;

  const getY = (mood) => {
    const idx = moodLevels.indexOf(mood);
    const level = idx === -1 ? 1 : idx; // по умолчанию "сонное"
    // 0 = злое (внизу), 2 = бодрое (вверху)
    return margin.top + (maxMoodIndex - level) * stepY;
  };

  const getX = (i) => margin.left + i * stepX;

  const points = moods
    .map((m, i) => `${getX(i)},${getY(m)}`)
    .join(" ");

  return (
    <svg
      className="mood-chart"
      viewBox={`0 0 ${width} ${height}`}
      role="img"
      aria-label="График настроения по дням недели"
    >
      {/* горизонтальная сетка и подписи уровней настроения */}
      {moodLevels.map((level, i) => {
        const y = margin.top + (maxMoodIndex - i) * stepY;
        return (
          <g key={level}>
            <line
              x1={margin.left}
              y1={y}
              x2={margin.left + innerWidth}
              y2={y}
              stroke="#9ca3af"
              strokeWidth="0.5"
            />
            <text
              x={margin.left - 10}
              y={y}
              className="mood-chart-label mood-chart-label--mood"
              dominantBaseline="middle"
            >
              {level}
            </text>
          </g>
        );
      })}

      {/* вертикальная сетка и подписи дней недели */}
      {moods.map((_, i) => {
        const x = getX(i);
        return (
          <g key={i}>
            <line
              x1={x}
              y1={margin.top}
              x2={x}
              y2={margin.top + innerHeight}
              stroke="rgba(148,163,184,0.4)"
              strokeWidth="0.5"
            />
            <text
              x={x}
              y={margin.top + innerHeight + 18}
              className="mood-chart-label mood-chart-label--day"
            >
              {dayNames[i]}
            </text>
          </g>
        );
      })}

      {/* линия настроения */}
      <polyline
        points={points}
        fill="none"
        stroke="#22c55e"
        strokeWidth="2"
      />

      {/* точки на линии */}
      {moods.map((m, i) => (
        <circle
          key={i}
          cx={getX(i)}
          cy={getY(m)}
          r="3"
          fill="#22c55e"
          stroke="#000000"
          strokeWidth="1"
        />
      ))}
    </svg>
  );
}

/* ===== ОСНОВНОЙ КОМПОНЕНТ APP ===== */

function App() {
  const [tab, setTab] = useState(TABS.TRAINING);

  // настройки тренировки
  const [mood, setMood] = useState("злое");
  const [mode, setMode] = useState("минималка");
  const [duration, setDuration] = useState("30:00");

  const moodOptions = ["злое", "сонное", "бодрое"];
  const modeOptions = ["минималка", "тихий апгрейд", "турбо"];
  const [pingStatus, setPingStatus] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/ping")
      .then((res) => res.json())
      .then((data) => {
        console.log("Ответ бэка:", data);
        setPingStatus(data.status);
      })
      .catch(() => setPingStatus("error"));
  }, []);
  
  const currentMoodImg = moodToImage[mood];

  // авторизация
  const [isAuthed, setIsAuthed] = useState(false);
  const [authMessage, setAuthMessage] = useState("");

  // история
  const [selectedHistoryId, setSelectedHistoryId] = useState(null);

  // сессия тренировки
  const [isTrainingSession, setIsTrainingSession] = useState(false);
  const [sessionPaused, setSessionPaused] = useState(false);
  const [sessionElapsed, setSessionElapsed] = useState(0);
  const [sessionTotal, setSessionTotal] = useState(30 * 60);
  const [currentSet, setCurrentSet] = useState(1);
  const [repsPerSet] = useState(12);

  // таймер
  useEffect(() => {
    if (!isTrainingSession || sessionPaused) return;

    const id = setInterval(() => {
      setSessionElapsed((prev) => {
        if (prev + 1 >= sessionTotal) {
          clearInterval(id);
          setIsTrainingSession(false);
          return sessionTotal;
        }
        return prev + 1;
      });
    }, 1000);

    return () => clearInterval(id);
  }, [isTrainingSession, sessionPaused, sessionTotal]);

  const handleDurationChange = (e) => {
    const raw = e.target.value.replace(/[^\d:]/g, "");
    if (raw.length <= 5) {
      setDuration(raw);
    }
  };

  const handleStart = (e) => {
    e.preventDefault();
    const totalSec = parseDurationToSeconds(duration || "30:00");
    setSessionTotal(totalSec);
    setSessionElapsed(0);
    setSessionPaused(false);
    setCurrentSet(1);
    setIsTrainingSession(true);
  };

  const handleTogglePause = () => {
    setSessionPaused((p) => !p);
  };

  const handleExerciseDone = () => {
    setCurrentSet((prev) => prev + 1);
  };

  const handleExerciseSkip = () => {
    setCurrentSet((prev) => prev + 1);
  };

  const handleFakeLogin = () => {
    if (!isAuthed) {
      setIsAuthed(true);
      setAuthMessage("Авторизация выполнена. История и статистика теперь доступны.");
    }
  };

  const handleTabClick = (targetTab) => {
    if (targetTab === TABS.TRAINING) {
      setTab(targetTab);
      setSelectedHistoryId(null);
      return;
    }

    if (!isAuthed) {
      setAuthMessage("Чтобы посмотреть историю и статистику, войдите в аккаунт.");
      return;
    }

    setTab(targetTab);
    setSelectedHistoryId(null);
  };

  /* ----- ЭКРАН ТРЕНИРОВКИ: НАСТРОЙКА ----- */

  const renderTrainingSetup = () => (
    <div className="ov-training-card">
      <div className="ov-avatar-big">
        {currentMoodImg && (
          <img
            src={currentMoodImg}
            alt={`аватар: ${mood}`}
            className="ov-avatar-img"
          />
        )}
      </div>

      <section className="ov-section">
        <div className="ov-section-caption">настроение</div>
        <div className="ov-options-row">
          {moodOptions.map((option) => (
            <button
              key={option}
              type="button"
              className={
                "ov-option-btn" +
                (mood === option ? " ov-option-btn--active" : "")
              }
              onClick={() => setMood(option)}
            >
              {option}
            </button>
          ))}
        </div>
      </section>

      <section className="ov-section">
        <div className="ov-section-caption">режим трени</div>
        <div className="ov-options-row">
          {modeOptions.map((option) => (
            <button
              key={option}
              type="button"
              className={
                "ov-option-btn" +
                (mode === option ? " ov-option-btn--active" : "")
              }
              onClick={() => setMode(option)}
            >
              {option}
            </button>
          ))}
        </div>
      </section>

      <section className="ov-section ov-section-duration">
        <div className="ov-section-caption">длительность</div>
        <input
          type="text"
          className="ov-duration-input"
          value={duration}
          onChange={handleDurationChange}
        />
      </section>

      <button className="ov-start-btn" onClick={handleStart}>
        старт
      </button>
    </div>
  );

  /* ----- ЭКРАН ТРЕНИРОВКИ: СЕССИЯ ----- */

  const renderTrainingSession = () => (
    <div className="training-session">
      <div className="training-session-caption">времени тренируешься:</div>

      <div className="training-session-timer">
        {formatSeconds(sessionElapsed)} / {formatSeconds(sessionTotal)}
      </div>

      <button
        type="button"
        className="training-session-pause-btn"
        onClick={handleTogglePause}
      >
        {sessionPaused ? "продолжить" : "пауза"}
      </button>

      <div className="ov-avatar-big">
        <img
          src={currentMoodImg}
          alt="эмоция тренировки"
          className="ov-avatar-img"
        />
      </div>

      <div className="training-session-quote">
        Наруто учил никогда не сдаваться
      </div>

      <div className="training-session-reps">x{repsPerSet}</div>

      <div className="training-session-set-caption">подход</div>
      <div className="training-session-set-number">{currentSet}</div>

      <div className="training-session-actions">
        <button
          type="button"
          className="training-btn training-btn--green"
          onClick={handleExerciseDone}
        >
          сделано
        </button>
        <button
          type="button"
          className="training-btn training-btn--red"
          onClick={handleExerciseSkip}
        >
          пропустить
        </button>
      </div>
    </div>
  );

  const renderTraining = () =>
    isTrainingSession ? renderTrainingSession() : renderTrainingSetup();

  /* ----- ИСТОРИЯ ----- */

  const renderHistoryList = () => (
    <div className="history-wrapper">
      <div className="history-header-row">
        <span>когда?</span>
        <span>настроение</span>
        <span>режим трени</span>
      </div>

      <div className="history-table">
        {historyData.map((entry) => (
          <div
            key={entry.id}
            className="history-row"
            onClick={() => setSelectedHistoryId(entry.id)}
          >
            <div className="history-cell">
              <div className="history-box history-box--date history-box--clickable">
                {entry.datetime}
              </div>
            </div>

            <div className="history-cell">
              <div className="history-box history-box--mood history-box--clickable">
                <div className="history-mood-inner">
                  <img
                    src={moodToImage[entry.mood]}
                    alt={entry.mood}
                    className="history-avatar"
                  />
                  <span>{entry.mood}</span>
                </div>
              </div>
            </div>

            <div className="history-cell">
              <div className="history-box history-box--mode history-box--clickable">
                {entry.mode}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderHistoryDetails = (entry) => (
    <div className="history-detail">
      <button
        type="button"
        className="history-back-btn"
        onClick={() => setSelectedHistoryId(null)}
      >
        ←
      </button>

      <div className="history-detail-top">
        <div className="history-detail-avatar">
          <img
            src={moodToImage[entry.mood]}
            alt={entry.mood}
            className="history-detail-avatar-img"
          />
        </div>

        <div className="history-detail-card">
          <div className="history-detail-card-title">данные о тренировке</div>

          <div className="history-detail-row">
            <span className="history-detail-label">когда:</span>
            <span className="history-detail-value">{entry.datetime}</span>
          </div>

          <div className="history-detail-row">
            <span className="history-detail-label">настроение:</span>
            <span className="history-detail-value">{entry.mood}</span>
          </div>

          <div className="history-detail-row">
            <span className="history-detail-label">режим трени:</span>
            <span className="history-detail-value">{entry.mode}</span>
          </div>

          <div className="history-detail-row">
            <span className="history-detail-label">всего баллов:</span>
            <span className="history-detail-value history-detail-value--green">
              {entry.totalPoints}
            </span>
          </div>
        </div>
      </div>

      <div className="history-detail-exercises">
        <div className="history-detail-exercises-title">
          Какие упражнения были?
        </div>

        <div className="history-detail-exercises-table">
          {entry.exercises.map((ex, index) => {
            const isZero = ex.sets === 0;
            return (
              <div key={index} className="history-detail-ex-row">
                <div
                  className={
                    "history-detail-ex-sets " +
                    (isZero
                      ? "history-detail-ex-sets--zero"
                      : "history-detail-ex-sets--ok")
                  }
                >
                  {ex.sets} подходов
                </div>
                <div className="history-detail-ex-name">{ex.name}</div>
                <div className="history-detail-ex-status">{ex.status}</div>
                <div className="history-detail-ex-points">
                  {ex.points} балла
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );

  const renderHistory = () => {
    const selectedEntry = historyData.find(
      (h) => h.id === selectedHistoryId
    );
    if (selectedEntry) return renderHistoryDetails(selectedEntry);
    return renderHistoryList();
  };

  /* ----- СТАТИСТИКА ----- */

  const renderStats = () => (
    <div className="stats-wrapper">
      <div className="stats-top">
        <div className="stats-badge">
          <StatsRadar flexibility={95} strength={60} endurance={55} />
        </div>

        <div className="stats-card">
          <div className="stats-card-header">
            <div className="stats-title">
              <div>ГИБКАЯ</div>
              <div>КОШЕЧКА</div>
            </div>
            <img src={catImg} alt="котик" className="stats-cat-icon" />
          </div>

          <div className="stats-card-body">
            <div className="stats-card-row">
              <span className="stats-label">стрик:</span>
              <span className="stats-value">345 дней</span>
            </div>
            <div className="stats-card-row">
              <span className="stats-label">любимый режим:</span>
              <span className="stats-value">минималка</span>
            </div>
            <div className="stats-card-row">
              <span className="stats-label">всего баллов:</span>
              <span className="stats-value">243</span>
            </div>
          </div>
        </div>
      </div>

      <div className="stats-mood-block">
        <div className="stats-mood-caption">настроение</div>
        <div className="mood-chart-container">
          <MoodChart moods={weekMoods} />
        </div>
      </div>
    </div>
  );

  /* ----- ОБЩИЙ РЕНДЕР ----- */

  const renderContent = () => {
    if (tab === TABS.TRAINING) return renderTraining();
    if (tab === TABS.HISTORY) return renderHistory();
    if (tab === TABS.STATS) return renderStats();
    return null;
  };

  const mainInnerClass =
    "ov-main-inner " +
    (tab === TABS.TRAINING ? "ov-main-inner--narrow" : "ov-main-inner--wide");

  return (
    <div className="ov-app">
      <header className="ov-header">
        <div className="ov-logo">OVERDRIVE</div>

        <nav className="ov-nav">
          <button
            type="button"
            className={
              "ov-nav-item " +
              (tab === TABS.TRAINING ? "ov-nav-item--active" : "")
            }
            onClick={() => handleTabClick(TABS.TRAINING)}
          >
            тренировка
          </button>
          <button
            type="button"
            className={
              "ov-nav-item " +
              (tab === TABS.HISTORY ? "ov-nav-item--active" : "")
            }
            onClick={() => handleTabClick(TABS.HISTORY)}
          >
            история
          </button>
          <button
            type="button"
            className={
              "ov-nav-item " +
              (tab === TABS.STATS ? "ov-nav-item--active" : "")
            }
            onClick={() => handleTabClick(TABS.STATS)}
          >
            статистика
          </button>
        </nav>

        <div className="ov-header-right">
          <button
            type="button"
            className="ov-login-btn"
            onClick={handleFakeLogin}
            disabled={isAuthed}
          >
            {isAuthed ? "В сети" : "Войти"}
          </button>

          <div className="ov-user-small">
            <img
              src={profileIcon}
              alt="Профиль"
              className="ov-user-icon"
            />
          </div>
        </div>
      </header>

      <main className="ov-main">
        {authMessage && (
          <div className="ov-auth-banner">
            <span className="ov-auth-text">{authMessage}</span>
            <button
              type="button"
              className="ov-auth-close"
              onClick={() => setAuthMessage("")}
              aria-label="Закрыть уведомление"
            >
              ×
            </button>
          </div>
        )}

        <div className={mainInnerClass}>{renderContent()}</div>
      </main>
    </div>
  );
}

export default App;
