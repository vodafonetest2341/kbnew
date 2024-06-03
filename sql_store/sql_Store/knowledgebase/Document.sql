CREATE TABLE [knowledgebase].[Document] (
    [ID]                 INT            IDENTITY (1, 1) NOT NULL,
    [Name]               VARCHAR (200)  NOT NULL,
    [Version]            VARCHAR (50)   NULL,
    [CheckSum]           VARCHAR (300)  NOT NULL,
    [Datasource]         INT            NOT NULL,
    [Destination]        VARCHAR (200)  NOT NULL,
    [LastDownloadedTime] DATETIME       NOT NULL,
    [AccessRights]       VARCHAR (1000) NULL,
    [Status]             VARCHAR (200)  NOT NULL,
    [Classification]     VARCHAR (200)  NOT NULL,
    [UpdatedAt]          DATETIME       CONSTRAINT [DF_Document] DEFAULT (getdate()) NOT NULL,
    [CreatedAt]          DATETIME       CONSTRAINT [DF_Document_CrAt] DEFAULT (getdate()) NULL,
    PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [DataSource_FK1] FOREIGN KEY ([Datasource]) REFERENCES [knowledgebase].[DataSource] ([ID]),
    CONSTRAINT [UC_CheckSum] UNIQUE NONCLUSTERED ([CheckSum] ASC),
    CONSTRAINT [UC_Destination] UNIQUE NONCLUSTERED ([Destination] ASC)
);


GO

