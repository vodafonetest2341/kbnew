CREATE TABLE [knowledgebase].[DataSource] (
    [ID]        INT           IDENTITY (1, 1) NOT NULL,
    [Name]      VARCHAR (500) NOT NULL,
    [Location]  VARCHAR (500) NOT NULL,
    [CreatedAt] DATETIME      CONSTRAINT [DF_DataSource_CrAt] DEFAULT (getdate()) NULL,
    [UpdatedAt] DATETIME      CONSTRAINT [DF_DataSource] DEFAULT (getdate()) NULL,
    PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO

