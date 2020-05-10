-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`GAMING_PLATFORM`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GAMING_PLATFORM` (
  `gaming_platform_id` INT NOT NULL,
  `platform_name` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`gaming_platform_id`),
  UNIQUE INDEX `platformName_UNIQUE` (`platform_name` ASC))
ENGINE = InnoDB
COMMENT = 'The platform that the WarFrame account is bound to. Example, PC, XBOX.';


-- -----------------------------------------------------
-- Table `mydb`.`WARFRAME_ACCOUNT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`WARFRAME_ACCOUNT` (
  `warframe_account_id` INT NULL,
  `warframe_alias` VARCHAR(45) NOT NULL,
  `is_blocked` TINYINT NOT NULL DEFAULT 0,
  `gaming_platform_id` INT NOT NULL,
  UNIQUE INDEX `waframeUserName_UNIQUE` (`warframe_alias` ASC),
  PRIMARY KEY (`warframe_account_id`),
  INDEX `gamingPlatform_fk_idx` (`gaming_platform_id` ASC),
  CONSTRAINT `gaming_platform_id_fk`
    FOREIGN KEY (`gaming_platform_id`)
    REFERENCES `mydb`.`GAMING_PLATFORM` (`gaming_platform_id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`USER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`USER` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `email_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `linked_warframe_account_id` INT NOT NULL,
  `beta_tester` TINYINT NOT NULL DEFAULT 0 COMMENT 'True is the user was a beta tester during beta testing. False otherwise.',
  `email_verificaiton_code` CHAR(32) NOT NULL COMMENT 'Verification code sent to a newly registered user\'s email address to verify the email.',
  `warframe_account_verification_code` VARCHAR(12) NOT NULL COMMENT 'Code used to verify a user\'s warframe account for users that want to link a warframe account to a [WEBSITE NAME] user account. This code is used by a bot that web scrapes the accounts messages on WarFrame\'s forum.\n\nIf a user messages a warframe forum bot this code, the warframe bot knows that the warframe account belongs to this USER. As such a relationship should be established between a WARFRAME_ACCOUNT and the USER.\n\nFor implementation, this field might have to be set to null by default and only be set when a user requests that his profile be linked to an account. When the user makes this request, the verificaition code is set. When the verirication code is set, and the user links his account by successfully messaging the bot the correct code, the account is linked and this field is set to NULL.',
  `is_staff` TINYINT(1) NOT NULL DEFAULT 0,
  `is_active` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `UserID_UNIQUE` (`user_id` ASC),
  UNIQUE INDEX `Email_UNIQUE` (`email` ASC),
  INDEX `warframeAccountID_fk_idx` (`linked_warframe_account_id` ASC),
  UNIQUE INDEX `linkedWarframeAccountID_UNIQUE` (`linked_warframe_account_id` ASC),
  UNIQUE INDEX `userVerificationEmailCode_UNIQUE` (`email_verificaiton_code` ASC),
  UNIQUE INDEX `warframeAccountVerificationCode_UNIQUE` (`warframe_account_verification_code` ASC),
  CONSTRAINT `linked_warframe_account_id_fk`
    FOREIGN KEY (`linked_warframe_account_id`)
    REFERENCES `mydb`.`WARFRAME_ACCOUNT` (`warframe_account_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`RELIC`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`RELIC` (
  `relic_id` INT NOT NULL AUTO_INCREMENT,
  `relic_name` VARCHAR(32) NOT NULL,
  `wiki_url` VARCHAR(256) NULL COMMENT 'wikiURL - A wiki url, representing the page corresponding to this relic. Usually used to provide a convenient link for the user to view information about this particular relic.',
  PRIMARY KEY (`relic_id`),
  UNIQUE INDEX `relicName_UNIQUE` (`relic_name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CHAT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CHAT` (
  `chatID` INT NOT NULL AUTO_INCREMENT,
  `dateCreated` DATETIME NOT NULL,
  `personOneUserID` INT NOT NULL,
  `personTwoUserID` INT NOT NULL,
  `personOneStillInChat` TINYINT NOT NULL DEFAULT 1,
  `personTwoStillInChat` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`chatID`),
  INDEX `user_fk_idx` (`personOneUserID` ASC),
  INDEX `user_fk_2_idx` (`personTwoUserID` ASC),
  CONSTRAINT `user_fk_1`
    FOREIGN KEY (`personOneUserID`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_fk_2`
    FOREIGN KEY (`personTwoUserID`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`CHAT_MESSAGE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`CHAT_MESSAGE` (
  `chatMessageID` INT NOT NULL,
  `chatID` INT NOT NULL,
  `fromUserID` INT NOT NULL,
  `message` VARCHAR(45) NOT NULL,
  `messageCreated` DATETIME NOT NULL,
  PRIMARY KEY (`chatMessageID`),
  INDEX `userID_fk_idx` (`fromUserID` ASC),
  INDEX `chatID_fk_idx` (`chatID` ASC),
  CONSTRAINT `chatID_fk`
    FOREIGN KEY (`chatID`)
    REFERENCES `mydb`.`CHAT` (`chatID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `userID_fk`
    FOREIGN KEY (`fromUserID`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`RUN_TYPE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`RUN_TYPE` (
  `runTypeID` INT NULL,
  `typeName` VARCHAR(32) NOT NULL COMMENT 'The type of relic run, such as 1 by 1, 2 by 2, or 4 by 4.',
  PRIMARY KEY (`runTypeID`),
  UNIQUE INDEX `typeName_UNIQUE` (`typeName` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`GROUP`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`GROUP` (
  `group_id` INT NOT NULL,
  `host_user_id` INT NOT NULL,
  `relic_id` INT NOT NULL,
  `run_type_id` INT NOT NULL,
  `players_in_group` INT NOT NULL,
  PRIMARY KEY (`group_id`),
  INDEX `relic_id_fk` (`relic_id` ASC),
  INDEX `runTypeID_fk_idx` (`run_type_id` ASC),
  INDEX `host_user_id_fk_idx` (`host_user_id` ASC),
  CONSTRAINT `relic_id_fk`
    FOREIGN KEY (`relic_id`)
    REFERENCES `mydb`.`RELIC` (`relic_id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `run_type_id_fk`
    FOREIGN KEY (`run_type_id`)
    REFERENCES `mydb`.`RUN_TYPE` (`runTypeID`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `host_user_id_fk`
    FOREIGN KEY (`host_user_id`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`OWNED_RELIC`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`OWNED_RELIC` (
  `ownedRelicID` INT NOT NULL,
  `userID` INT NOT NULL,
  `relicID` INT NOT NULL,
  PRIMARY KEY (`ownedRelicID`),
  INDEX `userID_fk_idx` (`userID` ASC),
  INDEX `relicID_fk_idx` (`relicID` ASC),
  CONSTRAINT `userID_fk`
    FOREIGN KEY (`userID`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `relicID_fk`
    FOREIGN KEY (`relicID`)
    REFERENCES `mydb`.`RELIC` (`relic_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ZOLD_USER_SCAM_INDICATOR`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ZOLD_USER_SCAM_INDICATOR` (
  `userStatusID` INT NOT NULL,
  `statusName` VARCHAR(45) NOT NULL,
  `userID` VARCHAR(45) NULL,
  UNIQUE INDEX `statusName_UNIQUE` (`statusName` ASC))
ENGINE = InnoDB
COMMENT = 'A user\'s status, such as Ready or Offline.\n\nA user that is \'Ready\' is online and ready to run relics.\n\nA user that is \'Offline\' is likely uninterested in running relics currently or is actually offline.';


-- -----------------------------------------------------
-- Table `mydb`.`REPORT_STATE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`REPORT_STATE` (
  `reportStateID` INT NOT NULL,
  `reportState` VARCHAR(45) NULL COMMENT 'The name of the status, such as \"being reviewed\", \"reviewed\", \"canceled\", etc.',
  PRIMARY KEY (`reportStateID`))
ENGINE = InnoDB
COMMENT = 'The status of a report case. For example, in review, reviewed, waiting, etc.';


-- -----------------------------------------------------
-- Table `mydb`.`REPORT_CASE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`REPORT_CASE` (
  `report_case_id` INT NOT NULL,
  `from_user_id` INT NOT NULL COMMENT 'The user that is doing the reporting.',
  `towards_user_id` INT NOT NULL COMMENT 'The user that is being reported.',
  `report_state_id` INT NOT NULL,
  PRIMARY KEY (`report_case_id`),
  UNIQUE INDEX `towardsUserID_UNIQUE` (`towards_user_id` ASC),
  INDEX `reportStatus_fk_idx` (`report_state_id` ASC),
  INDEX `fromUserID_fk_idx` (`from_user_id` ASC),
  CONSTRAINT `report_state_id_fk`
    FOREIGN KEY (`report_state_id`)
    REFERENCES `mydb`.`REPORT_STATE` (`reportStateID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `from_user_id_fk`
    FOREIGN KEY (`from_user_id`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `towards_user_id_fk`
    FOREIGN KEY (`towards_user_id`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'A report sent by \"fromUser\" to \"towardsUser\" to flag \"towardsUser\'s\" account. Flagging a user\'s account warns other players if \"towardsUser\" has made any offenses in the past.';


-- -----------------------------------------------------
-- Table `mydb`.`ZOLD_USERNAME_RECOVERY`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ZOLD_USERNAME_RECOVERY` (
  `usernameRecoveryID` INT NOT NULL,
  `recoveryCode` VARCHAR(32) NOT NULL,
  `dateCodeCreated` DATETIME NOT NULL,
  `dateCodeUsed` DATETIME NULL,
  PRIMARY KEY (`usernameRecoveryID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`PASSWORD_RECOVERY`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`PASSWORD_RECOVERY` (
  `password_recovery_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `recovery_code` VARCHAR(32) NOT NULL,
  `dateCodeCreated` DATETIME NOT NULL,
  `dateCodeUsed` DATETIME NOT NULL,
  PRIMARY KEY (`password_recovery_id`),
  INDEX `userID_fk_idx` (`user_id` ASC),
  UNIQUE INDEX `dateCodeUsed_UNIQUE` (`dateCodeUsed` ASC),
  CONSTRAINT `userID_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`USER` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ZDEP_REPORT_STATUS_STATE_TRANSITION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ZDEP_REPORT_STATUS_STATE_TRANSITION` (
  `reportStatusStateTransitionID` INT NOT NULL,
  `stateName` VARCHAR(45) NOT NULL,
  `event` VARCHAR(45) NOT NULL,
  `stateTransition` VARCHAR(45) NOT NULL,
  `REPORT_STATUS_STATE_TRANSITION_reportStatusStateTransitionID` INT NOT NULL,
  `REPORT_STATUS_STATE_TRANSITION_reportStatusStateTransitionID1` INT NOT NULL,
  PRIMARY KEY (`reportStatusStateTransitionID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`REPORT_STATUS_STATE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`REPORT_STATUS_STATE` (
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`IMAGE_PROOF`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`IMAGE_PROOF` (
  `imageProofID` INT NOT NULL AUTO_INCREMENT,
  `imageURLPath` VARCHAR(45) NOT NULL,
  `reportCaseID` INT NOT NULL,
  PRIMARY KEY (`imageProofID`),
  UNIQUE INDEX `imageURLPath_UNIQUE` (`imageURLPath` ASC),
  INDEX `reportCaseID_fk_idx` (`reportCaseID` ASC),
  CONSTRAINT `reportCaseID_fk`
    FOREIGN KEY (`reportCaseID`)
    REFERENCES `mydb`.`REPORT_CASE` (`report_case_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`VIDEO_PROOF`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`VIDEO_PROOF` (
  `videoProofID` INT NOT NULL,
  `videoLink` VARCHAR(512) NULL,
  `reportCaseID` INT NOT NULL,
  PRIMARY KEY (`videoProofID`),
  INDEX `reportCaseID_fk_idx` (`reportCaseID` ASC),
  CONSTRAINT `reportCaseID_fk`
    FOREIGN KEY (`reportCaseID`)
    REFERENCES `mydb`.`REPORT_CASE` (`report_case_id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ZOLD_EMAIL_VERIFICATION_CODE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ZOLD_EMAIL_VERIFICATION_CODE` (
  `email_verification_code_id` INT NOT NULL,
  `email_verification_code` VARCHAR(32) NULL DEFAULT 'django-function',
  PRIMARY KEY (`email_verification_code_id`),
  UNIQUE INDEX `email_verification_code_UNIQUE` (`email_verification_code` ASC))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
