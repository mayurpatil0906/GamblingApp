GAMBLERS_TABLE = """CREATE TABLE IF NOT EXISTS gamblers (
        gambler_id BIGINT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        full_name VARCHAR(150) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        is_active BOOLEAN NOT NULL,
        initial_stake DECIMAL(12,2) NOT NULL,
        current_stake DECIMAL(12,2) NOT NULL,
        win_threshold DECIMAL(12,2) NOT NULL,
        loss_threshold DECIMAL(12,2) NOT NULL,
        min_required_stake DECIMAL(12,2) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    )"""

BETTING_PREFERENCES_TABLE = """CREATE TABLE IF NOT EXISTS betting_preferences (
        preference_id BIGINT PRIMARY KEY,
        gambler_id BIGINT UNIQUE,
        min_bet DECIMAL(12,2) NOT NULL,
        max_bet DECIMAL(12,2) NOT NULL,
        preferred_game_type VARCHAR(100),
        auto_play_enabled BOOLEAN NOT NULL,
        auto_play_max_games INT NOT NULL,
        session_loss_limit DECIMAL(12,2) NOT NULL,
        session_win_target DECIMAL(12,2) NOT NULL,
        updated_at DATETIME NOT NULL,
        CONSTRAINT fk_betting_preferences_gambler
            FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
    )"""

SESSIONS_TABLE = """CREATE TABLE IF NOT EXISTS sessions (
        session_id BIGINT PRIMARY KEY,
        gambler_id BIGINT NOT NULL,
        status VARCHAR(50) NOT NULL,
        end_reason VARCHAR(100),
        starting_stake DECIMAL(12,2) NOT NULL,
        ending_stake DECIMAL(12,2) NOT NULL,
        peak_stake DECIMAL(12,2) NOT NULL,
        lowest_stake DECIMAL(12,2) NOT NULL,
        max_games INT NOT NULL,
        games_played INT NOT NULL,
        total_pause_seconds INT NOT NULL,
        started_at DATETIME NOT NULL,
        ended_at DATETIME,
        created_at DATETIME NOT NULL,
        CONSTRAINT fk_sessions_gambler
            FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
    )"""

SESSION_PARAMETERS_TABLE = """CREATE TABLE IF NOT EXISTS session_parameters (
        parameter_id BIGINT PRIMARY KEY,
        session_id BIGINT NOT NULL,
        lower_limit DECIMAL(12,2) NOT NULL,
        upper_limit DECIMAL(12,2) NOT NULL,
        min_bet DECIMAL(12,2) NOT NULL,
        max_bet DECIMAL(12,2) NOT NULL,
        default_win_probability DECIMAL(5,2) NOT NULL,
        max_session_minutes INT NOT NULL,
        strict_mode BOOLEAN NOT NULL,
        created_at DATETIME NOT NULL,
        CONSTRAINT fk_session_parameters_session
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    )"""

BETTING_STRATEGIES_TABLE = """CREATE TABLE IF NOT EXISTS betting_strategies (
        strategy_id BIGINT PRIMARY KEY,
        strategy_name VARCHAR(100) NOT NULL,
        description VARCHAR(255),
        is_active BOOLEAN NOT NULL,
        created_at DATETIME NOT NULL
    )"""

ODDS_CONFIGURATION_TABLE = """CREATE TABLE IF NOT EXISTS odds_configuration (
        odds_config_id BIGINT PRIMARY KEY,
        odds_type VARCHAR(50) NOT NULL,
        fixed_multiplier DECIMAL(10,2),
        american_odds INT,
        decimal_odds DECIMAL(10,2),
        probability_payout_factor DECIMAL(10,2),
        house_edge DECIMAL(10,2),
        is_default BOOLEAN NOT NULL,
        created_at DATETIME NOT NULL
    )"""

BETS_TABLE = """CREATE TABLE IF NOT EXISTS bets (
        bet_id BIGINT PRIMARY KEY,
        session_id BIGINT NOT NULL,
        gambler_id BIGINT NOT NULL,
        strategy_id BIGINT NOT NULL,
        game_index INT NOT NULL,
        bet_amount DECIMAL(12,2) NOT NULL,
        win_probability DECIMAL(5,2) NOT NULL,
        odds_type VARCHAR(50) NOT NULL,
        odds_value DECIMAL(10,2) NOT NULL,
        potential_win DECIMAL(12,2) NOT NULL,
        stake_before DECIMAL(12,2) NOT NULL,
        stake_after DECIMAL(12,2) NOT NULL,
        is_settled BOOLEAN NOT NULL,
        placed_at DATETIME NOT NULL,
        CONSTRAINT fk_bets_session
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
        CONSTRAINT fk_bets_gambler
            FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id),
        CONSTRAINT fk_bets_strategy
            FOREIGN KEY (strategy_id) REFERENCES betting_strategies(strategy_id)
    )"""

GAME_RECORDS_TABLE = """CREATE TABLE IF NOT EXISTS game_records (
        game_id BIGINT PRIMARY KEY,
        session_id BIGINT NOT NULL,
        bet_id BIGINT NOT NULL,
        odds_config_id BIGINT NOT NULL,
        outcome VARCHAR(50) NOT NULL,
        payout_amount DECIMAL(12,2) NOT NULL,
        loss_amount DECIMAL(12,2) NOT NULL,
        net_change DECIMAL(12,2) NOT NULL,
        stake_before DECIMAL(12,2) NOT NULL,
        stake_after DECIMAL(12,2) NOT NULL,
        consecutive_win_streak INT NOT NULL,
        consecutive_loss_streak INT NOT NULL,
        game_duration_seconds INT NOT NULL,
        resolved_at DATETIME NOT NULL,
        CONSTRAINT fk_game_records_session
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
        CONSTRAINT fk_game_records_bet
            FOREIGN KEY (bet_id) REFERENCES bets(bet_id),
        CONSTRAINT fk_game_records_odds
            FOREIGN KEY (odds_config_id) REFERENCES odds_configuration(odds_config_id)
    )"""

STAKE_TRANSACTION_TABLE = """CREATE TABLE IF NOT EXISTS stake_transaction (
        transaction_id BIGINT PRIMARY KEY,
        gambler_id BIGINT NOT NULL,
        session_id BIGINT,
        bet_id BIGINT,
        transaction_type VARCHAR(50) NOT NULL,
        amount DECIMAL(12,2) NOT NULL,
        balance_before DECIMAL(12,2) NOT NULL,
        balance_after DECIMAL(12,2) NOT NULL,
        created_at DATETIME NOT NULL,
        CONSTRAINT fk_stake_transaction_gambler
            FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id),
        CONSTRAINT fk_stake_transaction_session
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
        CONSTRAINT fk_stake_transaction_bet
            FOREIGN KEY (bet_id) REFERENCES bets(bet_id)
    )"""

PAUSE_RECORDS_TABLE = """CREATE TABLE IF NOT EXISTS pause_records (
        pause_id BIGINT PRIMARY KEY,
        session_id BIGINT NOT NULL,
        pause_reason VARCHAR(150) NOT NULL,
        paused_at DATETIME NOT NULL,
        resumed_at DATETIME,
        pause_seconds INT NOT NULL,
        CONSTRAINT fk_pause_records_session
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    )"""

RUNNING_TOTAL_SNAPSHOTS_TABLE = """CREATE TABLE IF NOT EXISTS running_total_snapshots (
        snapshot_id BIGINT PRIMARY KEY,
        session_id BIGINT NOT NULL,
        game_id BIGINT NOT NULL,
        total_games INT NOT NULL,
        total_wins INT NOT NULL,
        total_losses INT NOT NULL,
        total_pushes INT NOT NULL,
        total_winnings DECIMAL(12,2) NOT NULL,
        total_losses_amount DECIMAL(12,2) NOT NULL,
        net_profit DECIMAL(12,2) NOT NULL,
        win_rate DECIMAL(10,2) NOT NULL,
        profit_factor DECIMAL(10,2) NOT NULL,
        roi DECIMAL(10,2) NOT NULL,
        longest_win_streak INT NOT NULL,
        longest_loss_streak INT NOT NULL,
        created_at DATETIME NOT NULL,
        CONSTRAINT fk_running_total_snapshots_session
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
        CONSTRAINT fk_running_total_snapshots_game
            FOREIGN KEY (game_id) REFERENCES game_records(game_id)
    )"""

VALIDATION_EVENTS_TABLE = """CREATE TABLE IF NOT EXISTS validation_events (
        validation_id BIGINT PRIMARY KEY,
        session_id BIGINT,
        gambler_id BIGINT,
        error_type VARCHAR(100) NOT NULL,
        severity VARCHAR(50) NOT NULL,
        field_name VARCHAR(100) NOT NULL,
        attempted_value VARCHAR(100) NOT NULL,
        message VARCHAR(255) NOT NULL,
        created_at DATETIME NOT NULL,
        CONSTRAINT fk_validation_events_session
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
        CONSTRAINT fk_validation_events_gambler
            FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
    )"""

ALL_TABLES = [
    GAMBLERS_TABLE,
    BETTING_PREFERENCES_TABLE,
    SESSIONS_TABLE,
    SESSION_PARAMETERS_TABLE,
    BETTING_STRATEGIES_TABLE,
    ODDS_CONFIGURATION_TABLE,
    BETS_TABLE,
    GAME_RECORDS_TABLE,
    STAKE_TRANSACTION_TABLE,
    PAUSE_RECORDS_TABLE,
    RUNNING_TOTAL_SNAPSHOTS_TABLE,
    VALIDATION_EVENTS_TABLE
]