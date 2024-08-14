DROP DATABASE IF EXISTS fontevote;
CREATE DATABASE IF NOT EXISTS fontevote;
USE fontevote;

CREATE TABLE IF NOT EXISTS candidate (
    candidateId INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    politicalAffiliation VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    educationLevel VARCHAR(255) NOT NULL,
    homeState VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS votingCenter (
    votingCenterId INT AUTO_INCREMENT PRIMARY KEY,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    zipcode INT NOT NULL
);

CREATE TABLE IF NOT EXISTS voter (
    voterId INT AUTO_INCREMENT PRIMARY KEY,
    politicalAffiliation VARCHAR(200),
    state VARCHAR(200),
    county VARCHAR(200),
    age INT,
    incomeLevel VARCHAR(200),
    ethnicity VARCHAR(200),
    gender VARCHAR(200),
    candidateId INT NOT NULL,
    votingCenterId INT,
    FOREIGN KEY (candidateId)
        REFERENCES candidate(candidateId)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT fk_voter_votingcenter
        FOREIGN KEY (votingCenterId)
            REFERENCES votingCenter(votingCenterId)
                ON UPDATE RESTRICT
                ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS campaign (
    campaignId INTEGER AUTO_INCREMENT PRIMARY KEY,
    newVotersRegistered INTEGER NOT NULL,
    dateLaunched DATE,
    candidateId INTEGER NOT NULL,
    CONSTRAINT camp_fk FOREIGN KEY (candidateId)
        REFERENCES candidate(candidateId)
            ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS campaignManagerSiteSurvey (
    campaignSurveyId INT AUTO_INCREMENT PRIMARY KEY,
    discoveredWhere VARCHAR(255) NOT NULL,-- how did you discover us?
    addAdditionalData TEXT NOT NULL,      -- what additional data would have been helpful for PollPal to provide?
    isDataUseful BOOLEAN NOT NULL,        -- was the data provided by PollPal useful for your campaign efforts?
    foundNeededInfo INT NOT NULL,         -- on a scale of 1-10, how user friendly was the site?
    isUserFriendly INT NOT NULL,          -- on a scale of 1-10, how much of the info we provided, met your needs?
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    campaignId INT,
    FOREIGN KEY (campaignId)
        REFERENCES campaign(campaignId)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS campaignFeaturesAccessed (
    surveyId INT,
    featureAccessed VARCHAR(255) NOT NULL,
    PRIMARY KEY (surveyId, featureAccessed),
    FOREIGN KEY(surveyId) REFERENCES campaignManagerSiteSurvey(campaignSurveyId)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS policy (
    policyId INT AUTO_INCREMENT PRIMARY KEY,
    policyName VARCHAR(250) NOT NULL,
    stance VARCHAR(250)
);

CREATE TABLE IF NOT EXISTS advocatesFor (
    policyId INT,
    candidateId INT,
    PRIMARY KEY (policyId, candidateId),
    FOREIGN KEY (candidateId) REFERENCES candidate(candidateId)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY (policyId) REFERENCES policy(policyId)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS voterSiteSurvey
(
    voterSurveyId INT AUTO_INCREMENT PRIMARY KEY,
    foundVotingCenter BOOLEAN NOT NULL,    -- did you find a voting center?
    isUserFriendly INT NOT NULL,           -- on a scale of 1-10, how user friendly was the site?
    foundNeededInfo INT NOT NULL,           -- on a scale of 1-10, how much of the info we provided met your needs?
    informedAboutCandidate BOOLEAN NOT NULL,  -- do you feel informed about the candidates?
    discoveredWhere VARCHAR(255) NOT NULL,          -- how did you discover us?
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    voterId INT NOT NULL,
    CONSTRAINT fk_voter_survey
       FOREIGN KEY (voterId)
           REFERENCES voter(voterId)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS voterFeaturesAccessed (
    surveyId INT,
    featureAccessed VARCHAR(255) NOT NULL,
    PRIMARY KEY (surveyId, featureAccessed),
    CONSTRAINT fk_voterFeature_survey
        FOREIGN KEY (surveyId)
            REFERENCES voterSiteSurvey(voterSurveyId)
                ON UPDATE CASCADE
                ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS advertisement (
    campaignId INTEGER,
    advertisementId INTEGER,
    location VARCHAR(255) NOT NULL,
    cost INTEGER NOT NULL,
    interactions INTEGER,
    PRIMARY KEY (campaignId, advertisementId),
    CONSTRAINT ad_fk FOREIGN KEY (campaignId)
        REFERENCES campaign(campaignId)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS rally (
    campaignId INTEGER,
    rallyId INTEGER,
    cost INTEGER NOT NULL,
    state VARCHAR(255) NOT NULL,
    volunteerCount INTEGER NOT NULL,
    expectedAttendance INTEGER,
    actualAttendance INTEGER,
    PRIMARY KEY (campaignId, rallyId),
    CONSTRAINT rally_fk FOREIGN KEY (campaignId)
        REFERENCES campaign(campaignId)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS election (
    electionId INT AUTO_INCREMENT PRIMARY KEY,
    year INT NOT NULL,
    winnerId INT,
    electoralVoteDifference INT,
    popularVoteDifference INT,
    CONSTRAINT fk_wid
        FOREIGN KEY (winnerId) REFERENCES candidate(candidateId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ranIn (
    electionId INT,
    candidateId INT,
    PRIMARY KEY (electionId, candidateId),
    CONSTRAINT fk_eid2
        FOREIGN KEY (electionId) REFERENCES election(electionId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
    CONSTRAINT fk_cid
        FOREIGN KEY (candidateId) REFERENCES candidate(candidateId)
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS stateResult (
    electionId INT,
    stateAbbr VARCHAR(10),
    stateName VARCHAR(255) NOT NULL,
    numElectoralVotes INT,
    popularVoteRatio FLOAT,
    voterTurnout FLOAT,
    partyRepresentative VARCHAR(255) NOT NULL,
    PRIMARY KEY (electionId, stateAbbr),
    CONSTRAINT fk_eID1
        FOREIGN KEY (electionId) REFERENCES election(electionId)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);
-- table for ml model
CREATE TABLE my_table (
    V201014b VARCHAR(255), V201228 VARCHAR(255), V201343 VARCHAR(255), 
    V201367 VARCHAR(255), V201409 VARCHAR(255), V201412 VARCHAR(255), 
    V201416 VARCHAR(255), V201417 VARCHAR(255), V201427 VARCHAR(255), 
    V201510 VARCHAR(255), V201575 VARCHAR(255), V201602 VARCHAR(255), 
    V201626 VARCHAR(255), V201627 VARCHAR(255), V201628 VARCHAR(255), 
    V202025 VARCHAR(255), V202172 VARCHAR(255), V202173 VARCHAR(255), 
    V202174 VARCHAR(255), V202224 VARCHAR(255), V202240 VARCHAR(255), 
    V202249 VARCHAR(255), V202257 VARCHAR(255), V202260 VARCHAR(255), 
    V202261 VARCHAR(255), V202262 VARCHAR(255), V202263 VARCHAR(255), 
    V202265 VARCHAR(255));


CREATE TABLE IF NOT EXISTS feature_importances (
    id INT PRIMARY KEY DEFAULT 0, 
    importances JSON
);

ALTER TABLE feature_importances
MODIFY id INT AUTO_INCREMENT PRIMARY KEY;
