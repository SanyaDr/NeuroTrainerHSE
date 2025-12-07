import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./App.css";

const TABS = {
  TRAINING: "training",
  HISTORY: "history",
  POINTS: "points",
};

function getEmotionLabel(value) {
  if (value <= -60) return "Очень неприятные";
  if (value <= -20) return "Неприятные";
  if (value < 20 && value > -20) return "Нейтральные";
  if (value < 60) return "Приятные";
  return "Очень приятные";
}

function EmotionTraining({ value, setValue }) {
  const emotionLabel = getEmotionLabel(value);

  return (
    <motion.div
      key="training"
      className="od-main-inner"
      initial={{ opacity: 0, y: 20, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -10, scale: 0.97 }}
      transition={{ duration: 0.35 }}
    >
      <div className="emotion-panel">
        <h2 className="emotion-question">
          Как бы Вы сейчас описали свои ощущения?
        </h2>

        <div className="emotion-circle-wrapper">
          <div className="emotion-circle">
            <div className="emotion-circle-inner" />
          </div>
        </div>

        <div className="emotion-label">{emotionLabel}</div>

        <div className="emotion-slider-block">
          <input
            type="range"
            min="-100"
            max="100"
            step="1"
            value={value}
            onChange={(e) => setValue(Number(e.target.value))}
            className="emotion-slider"
          />
          <div className="emotion-slider-caption">
            <span>ОЧЕНЬ НЕПРИЯТНЫЕ</span>
            <span>ОЧЕНЬ ПРИЯТНЫЕ</span>
          </div>
        </div>

        <button className="primary-btn" onClick={() => {}}>
          Далее
        </button>
      </div>
    </motion.div>
  );
}

function Placeholder({ title, subtitle }) {
  return (
    <motion.div
      key={title}
      className="od-main-inner"
      initial={{ opacity: 0, y: 20, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -10, scale: 0.97 }}
      transition={{ duration: 0.35 }}
    >
      <div className="placeholder-panel">
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
    </motion.div>
  );
}

function App() {
  const [tab, setTab] = useState(TABS.TRAINING);
  const [emotionValue, setEmotionValue] = useState(0);

  // --- состояние авторизации ---
  const [isAuthed, setIsAuthed] = useState(false);
  const [authMessage, setAuthMessage] = useState("");

  // заглушка авторизации (потом заменишь на реальную)
  const handleFakeLogin = () => {
    setIsAuthed(true);
    setAuthMessage("Авторизация выполнена. Теперь история и баллы доступны.");
    setTimeout(() => setAuthMessage(""), 3000);
  };

  const handleTabClick = (targetTab) => {
    if (targetTab === TABS.TRAINING) {
      setTab(targetTab);
      return;
    }

    if (!isAuthed) {
      // без авторизации не переключаемся на историю/баллы
      setAuthMessage("Чтобы посмотреть историю и баллы, войдите в аккаунт");
      // здесь можно открыть модалку логина
      return;
    }

    setTab(targetTab);
  };

  return (
    <div className="od-app">
      {/* Верхняя панель */}
      <header className="od-header">
        <div className="od-logo">OVERDRIVE</div>

        <nav className="od-nav">
          <button
            className={
              "od-nav-item " +
              (tab === TABS.TRAINING ? "od-nav-item--active" : "")
            }
            onClick={() => handleTabClick(TABS.TRAINING)}
          >
            Тренировка
          </button>
          <button
            className={
              "od-nav-item " +
              (tab === TABS.HISTORY ? "od-nav-item--active" : "")
            }
            onClick={() => handleTabClick(TABS.HISTORY)}
          >
            История
          </button>
          <button
            className={
              "od-nav-item " +
              (tab === TABS.POINTS ? "od-nav-item--active" : "")
            }
            onClick={() => handleTabClick(TABS.POINTS)}
          >
            Баллы
          </button>
        </nav>

        <div className="od-header-right">
          {/* временная кнопка "войти" вместо реальной авторизации */}
          <button
            className="od-login-btn"
            onClick={handleFakeLogin}
            disabled={isAuthed}
          >
            {isAuthed ? "В сети" : "Войти"}
          </button>

          <div className="od-user-icon">
            <div className="od-user-circle">
              <span className="od-user-initial">☺</span>
            </div>
          </div>
        </div>
      </header>

      {/* Основной контент на всю область окна */}
      <main className="od-main">
        <div className="od-bg-glow od-bg-glow-left" />
        <div className="od-bg-glow od-bg-glow-right" />

        {/* сообщение об отсутствии авторизации */}
       {authMessage && (
  <div className="od-auth-banner">
    <span className="od-auth-text">{authMessage}</span>
    <button
      className="od-auth-close"
      onClick={() => setAuthMessage("")}
      aria-label="Закрыть уведомление"
    >
      ×
    </button>
  </div>
)}


        <AnimatePresence mode="wait">
          {tab === TABS.TRAINING && (
            <EmotionTraining
              value={emotionValue}
              setValue={setEmotionValue}
            />
          )}

          {tab === TABS.HISTORY && (
            <Placeholder
              title="История"
              subtitle="Здесь появится таймлайн ваших тренировок."
            />
          )}

          {tab === TABS.POINTS && (
            <Placeholder
              title="Баллы"
              subtitle="Скоро здесь будут уровни, бонусы и статистика."
            />
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
